"""LangGraph-based Multi-Agent Orchestrator for YouTube Trends Analysis"""

from typing import Dict, Any, List, Optional, TypedDict, Annotated
from enum import Enum
import operator

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from loguru import logger

from .sql_agent import SQLAgent
from .vector_agent import VectorAgent
from .query_router import QueryRouter, QueryType
from ..config.settings import get_settings


class AgentState(TypedDict):
    """
    State object for the multi-agent workflow.
    Tracks the query, routing decisions, and results from each agent.
    """
    query: str
    routing_info: Dict[str, Any]
    sql_result: Optional[Dict[str, Any]]
    vector_result: Optional[Dict[str, Any]]
    final_response: Optional[str]
    error: Optional[str]
    metadata: Dict[str, Any]


class WorkflowStage(str, Enum):
    """Enum for workflow stages"""
    ROUTE = "route"
    SQL_AGENT = "sql_agent"
    VECTOR_AGENT = "vector_agent"
    SYNTHESIZE = "synthesize"
    END = "end"


class MultiAgentOrchestrator:
    """
    LangGraph-based orchestrator that manages multiple agents.
    
    Workflow:
    1. Route query to appropriate agent(s)
    2. Execute agent(s) in parallel or sequence
    3. Synthesize results into final response
    4. Return to user
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        enable_sql: bool = True,
        enable_vector: bool = True
    ):
        """
        Initialize Multi-Agent Orchestrator.
        
        Args:
            api_key: OpenAI/OpenRouter API key
            model: LLM model to use
            enable_sql: Enable SQL agent
            enable_vector: Enable Vector agent
        """
        settings = get_settings()
        
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.llm_model
        self.base_url = settings.openai_base_url
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set OPENAI_API_KEY in environment or .env file"
            )
        
        # Initialize components
        self.enable_sql = enable_sql
        self.enable_vector = enable_vector
        
        self._initialize_router()
        self._initialize_agents()
        self._initialize_llm()
        self._build_graph()
        
        logger.info("Multi-Agent Orchestrator initialized")
    
    def _initialize_router(self) -> None:
        """Initialize query router"""
        try:
            self.router = QueryRouter(
                api_key=self.api_key,
                model=self.model
            )
            logger.info("Query router initialized")
        except Exception as e:
            logger.error(f"Failed to initialize router: {e}")
            raise
    
    def _initialize_agents(self) -> None:
        """Initialize all agents"""
        self.agents = {}
        
        if self.enable_sql:
            try:
                self.agents['sql'] = SQLAgent(
                    api_key=self.api_key,
                    model=self.model
                )
                logger.info("SQL Agent initialized")
            except Exception as e:
                logger.warning(f"SQL Agent initialization failed: {e}")
                self.enable_sql = False
        
        if self.enable_vector:
            try:
                self.agents['vector'] = VectorAgent(
                    api_key=self.api_key,
                    model=self.model
                )
                logger.info("Vector Agent initialized")
            except Exception as e:
                logger.warning(f"Vector Agent initialization failed: {e}")
                self.enable_vector = False
        
        if not self.agents:
            raise RuntimeError("No agents could be initialized")
    
    def _initialize_llm(self) -> None:
        """Initialize LLM for response synthesis"""
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0.3,
            api_key=self.api_key,
            base_url=self.base_url
        )
        logger.info("Synthesis LLM initialized")
    
    def _build_graph(self) -> None:
        """Build LangGraph workflow"""
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("route", self._route_query)
        workflow.add_node("sql_agent", self._execute_sql_agent)
        workflow.add_node("vector_agent", self._execute_vector_agent)
        workflow.add_node("synthesize", self._synthesize_response)
        
        # Set entry point
        workflow.set_entry_point("route")
        
        # Add conditional edges from routing
        workflow.add_conditional_edges(
            "route",
            self._routing_decision,
            {
                "sql": "sql_agent",
                "vector": "vector_agent",
                "both": "sql_agent",  # Start with SQL for hybrid
                "end": END
            }
        )
        
        # Add edges from agents to synthesis
        # workflow.add_edge("sql_agent", self._check_if_hybrid)
        workflow.add_conditional_edges(
    "sql_agent",
    self._check_if_hybrid,
    {
        "vector_agent": "vector_agent",
        "synthesize": "synthesize"
    }
)


        workflow.add_edge("vector_agent", "synthesize")
        
        # Add edge from synthesis to end
        workflow.add_edge("synthesize", END)
        
        # Compile graph
        self.graph = workflow.compile()
        
        logger.info("LangGraph workflow built successfully")
    
    def _route_query(self, state: AgentState) -> AgentState:
        """
        Route the query to appropriate agent(s).
        
        Args:
            state: Current state
            
        Returns:
            Updated state with routing info
        """
        logger.info(f"Routing query: {state['query']}")
        
        try:
            routing_info = self.router.route_query(state['query'])
            state['routing_info'] = routing_info
            
            logger.info(
                f"Query routed to: {routing_info['agents']} "
                f"(type: {routing_info['classification']['type']})"
            )
            
        except Exception as e:
            logger.error(f"Routing error: {e}")
            state['error'] = f"Routing failed: {str(e)}"
            state['routing_info'] = {'agents': [], 'classification': {'type': 'unknown'}}
        
        return state
    
    def _routing_decision(self, state: AgentState) -> str:
        """
        Determine which path to take based on routing.
        
        Args:
            state: Current state
            
        Returns:
            Next node name
        """
        if state.get('error'):
            return "end"
        
        agents = state['routing_info'].get('agents', [])
        
        if not agents:
            return "end"
        elif 'sql' in agents and 'vector' in agents:
            return "both"
        elif 'sql' in agents:
            return "sql"
        elif 'vector' in agents:
            return "vector"
        else:
            return "end"
    
    def _execute_sql_agent(self, state: AgentState) -> AgentState:
        """
        Execute SQL agent.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with SQL results
        """
        logger.info("Executing SQL Agent")
        
        try:
            if 'sql' in self.agents:
                result = self.agents['sql'].process_query(state['query'])
                state['sql_result'] = result
                logger.info("SQL Agent execution complete")
            else:
                state['sql_result'] = {
                    'success': False,
                    'error': 'SQL Agent not available'
                }
        except Exception as e:
            logger.error(f"SQL Agent error: {e}")
            state['sql_result'] = {
                'success': False,
                'error': str(e)
            }
        
        return state
    
    def _execute_vector_agent(self, state: AgentState) -> AgentState:
        """
        Execute Vector agent.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with Vector results
        """
        logger.info("Executing Vector Agent")
        
        try:
            if 'vector' in self.agents:
                result = self.agents['vector'].process_query(state['query'])
                state['vector_result'] = result
                logger.info("Vector Agent execution complete")
            else:
                state['vector_result'] = {
                    'success': False,
                    'error': 'Vector Agent not available'
                }
        except Exception as e:
            logger.error(f"Vector Agent error: {e}")
            state['vector_result'] = {
                'success': False,
                'error': str(e)
            }
        
        return state
    
    def _check_if_hybrid(self, state: AgentState) -> str:
        """
        Check if we need to execute vector agent for hybrid query.
        
        Args:
            state: Current state
            
        Returns:
            Next node name
        """
        agents = state['routing_info'].get('agents', [])
        
        if 'vector' in agents and not state.get('vector_result'):
            return "vector_agent"
        else:
            return "synthesize"
    
    def _synthesize_response(self, state: AgentState) -> AgentState:
        """
        Synthesize final response from agent results.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with final response
        """
        logger.info("Synthesizing final response")
        
        try:
            sql_result = state.get('sql_result')
            vector_result = state.get('vector_result')
            
            # If only one agent was used, return its response
            if sql_result and not vector_result:
                if sql_result.get('success'):
                    state['final_response'] = sql_result['data']['answer']
                else:
                    state['final_response'] = f"Error: {sql_result.get('error', 'Unknown error')}"
            
            elif vector_result and not sql_result:
                if vector_result.get('success'):
                    state['final_response'] = vector_result['data']['answer']
                else:
                    state['final_response'] = f"Error: {vector_result.get('error', 'Unknown error')}"
            
            # If both agents were used, synthesize responses
            elif sql_result and vector_result:
                state['final_response'] = self._synthesize_hybrid_response(
                    state['query'],
                    sql_result,
                    vector_result
                )
            
            else:
                state['final_response'] = "I couldn't process your query. Please try rephrasing."
            
            # Add metadata
            state['metadata'] = {
                'agents_used': state['routing_info'].get('agents', []),
                'query_type': state['routing_info']['classification']['type'],
                'confidence': state['routing_info']['classification']['confidence']
            }
            
            logger.info("Response synthesis complete")
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            state['final_response'] = f"Error synthesizing response: {str(e)}"
        
        return state
    
    def _synthesize_hybrid_response(
        self,
        query: str,
        sql_result: Dict[str, Any],
        vector_result: Dict[str, Any]
    ) -> str:
        """
        Synthesize response from both SQL and Vector results.
        
        Args:
            query: Original query
            sql_result: SQL agent result
            vector_result: Vector agent result
            
        Returns:
            Synthesized response
        """
        try:
            sql_answer = sql_result.get('data', {}).get('answer', 'No SQL result')
            vector_answer = vector_result.get('data', {}).get('answer', 'No vector result')
            
            prompt = f"""You are a YouTube trends analyst. Synthesize the following results into a coherent, helpful response.

User Query: {query}

Structured Data Analysis (SQL):
{sql_answer}

Semantic Search Results (Vector):
{vector_answer}

Provide a unified response that:
1. Combines insights from both sources
2. Answers the user's question comprehensively
3. Highlights key findings
4. Keeps it concise and natural

Response:"""
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.error(f"Hybrid synthesis error: {e}")
            return f"SQL Analysis: {sql_answer}\n\nSemantic Search: {vector_answer}"
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a query through the multi-agent workflow.
        
        Args:
            query: User query
            
        Returns:
            Final response dictionary
        """
        logger.info(f"Processing query through orchestrator: {query}")
        
        # Initialize state
        initial_state: AgentState = {
            'query': query,
            'routing_info': {},
            'sql_result': None,
            'vector_result': None,
            'final_response': None,
            'error': None,
            'metadata': {}
        }
        
        try:
            # Execute workflow
            final_state = self.graph.invoke(initial_state)
            
            # Format response
            response = {
                'query': query,
                'answer': final_state.get('final_response', 'No response generated'),
                'metadata': final_state.get('metadata', {}),
                'routing': final_state.get('routing_info', {}),
                'success': final_state.get('final_response') is not None
            }
            
            # Include agent results if available
            if final_state.get('sql_result'):
                response['sql_result'] = final_state['sql_result']
            if final_state.get('vector_result'):
                response['vector_result'] = final_state['vector_result']
            
            logger.info("Query processing complete")
            return response
            
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            return {
                'query': query,
                'answer': f"An error occurred: {str(e)}",
                'metadata': {},
                'success': False,
                'error': str(e)
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about available agents.
        
        Returns:
            Agent information dictionary
        """
        info = {
            'orchestrator': 'LangGraph Multi-Agent System',
            'agents': {}
        }
        
        for name, agent in self.agents.items():
            info['agents'][name] = agent.get_capabilities()
        
        return info
