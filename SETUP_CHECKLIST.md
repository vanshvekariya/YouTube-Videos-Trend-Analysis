# Setup Checklist ✅

Use this checklist to ensure your multi-agent system is properly configured.

## 📋 Pre-Setup

- [ ] Python 3.8+ installed
  ```bash
  python --version
  ```

- [ ] Docker installed and running
  ```bash
  docker --version
  docker ps
  ```

- [ ] Git repository cloned
  ```bash
  cd YouTube-Videos-Trend-Analysis
  ```

## 🔧 Installation

- [ ] Virtual environment created
  ```bash
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Installation verified
  ```bash
  python -c "import langchain, langgraph, qdrant_client; print('✅ All imports successful')"
  ```

## 🔑 Configuration

- [ ] `.env` file created
  ```bash
  touch .env  # Windows: type nul > .env
  ```

- [ ] API key added to `.env`
  ```env
  OPENAI_API_KEY=your_api_key_here
  ```

- [ ] API key verified
  ```bash
  python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ API key loaded' if os.getenv('OPENAI_API_KEY') else '❌ API key missing')"
  ```

- [ ] Optional settings configured (if needed)
  ```env
  LLM_MODEL=anthropic/claude-3-haiku
  SQL_DB_PATH=youtube_trends_canada.db
  QDRANT_HOST=localhost
  QDRANT_PORT=6333
  ```

## 🗄️ Database Setup

- [ ] Qdrant started
  ```bash
  docker-compose up -d
  ```

- [ ] Qdrant running
  ```bash
  curl http://localhost:6333
  # Should return: {"title":"qdrant - vector search engine",...}
  ```

- [ ] Data file available
  ```bash
  ls data/raw/CAvideos.csv
  # Should show the CSV file
  ```

- [ ] Data processed
  ```bash
  python scripts/process_and_index.py --csv data/raw/CAvideos.csv
  ```

- [ ] SQL database created
  ```bash
  ls youtube_trends_canada.db
  # Should show the database file
  ```

- [ ] Vector database indexed
  ```bash
  # Check Qdrant dashboard: http://localhost:6333/dashboard
  # Or use API:
  curl http://localhost:6333/collections
  # Should show "youtube_trends" collection
  ```

## 🧪 Testing

- [ ] Import test passed
  ```bash
  python -c "from src.main import YouTubeTrendsApp; print('✅ Imports working')"
  ```

- [ ] System info accessible
  ```bash
  python -m src.main --info
  # Should display system information
  ```

- [ ] Test query works
  ```bash
  python -m src.main --query "How many videos are in the database?"
  # Should return an answer
  ```

- [ ] Unit tests pass
  ```bash
  pytest tests/test_multi_agent_system.py -v
  ```

## 🚀 Verification

- [ ] Interactive mode works
  ```bash
  python -m src.main
  # Should start interactive CLI
  # Type 'quit' to exit
  ```

- [ ] SQL queries work
  ```bash
  python -m src.main --query "Which category has the most videos?"
  # Should return SQL-based answer
  ```

- [ ] Vector queries work
  ```bash
  python -m src.main --query "Find videos about cooking"
  # Should return vector search results
  ```

- [ ] Hybrid queries work
  ```bash
  python -m src.main --query "Most popular gaming videos about Minecraft"
  # Should use both agents
  ```

- [ ] Python API works
  ```python
  from src.main import YouTubeTrendsApp
  app = YouTubeTrendsApp()
  response = app.query("Test query")
  print(response['answer'])
  # Should print an answer
  ```

## 📊 Logs & Monitoring

- [ ] Logs directory created
  ```bash
  ls logs/
  # Should show log files
  ```

- [ ] Logs are being written
  ```bash
  tail -f logs/youtube_trends_*.log
  # Should show recent log entries
  ```

- [ ] No critical errors in logs
  ```bash
  grep -i error logs/youtube_trends_*.log
  # Should show minimal or no errors
  ```

## 🎯 Optional Enhancements

- [ ] Custom model configured
  ```env
  LLM_MODEL=anthropic/claude-3-sonnet  # or other model
  ```

- [ ] Batch size optimized
  ```env
  BATCH_SIZE=200  # Adjust based on your system
  ```

- [ ] Additional data sources added
  ```bash
  # Process multiple CSV files
  python scripts/process_and_index.py --csv data/raw/USvideos.csv --country US
  ```

## 🐛 Troubleshooting Checklist

If something doesn't work, check:

- [ ] Python version is 3.8+
- [ ] All dependencies installed correctly
- [ ] `.env` file exists and has API key
- [ ] Qdrant is running (`docker ps | grep qdrant`)
- [ ] Data has been processed
- [ ] No firewall blocking port 6333
- [ ] Sufficient disk space for databases
- [ ] Virtual environment is activated

## 📝 Quick Commands Reference

```bash
# Start Qdrant
docker-compose up -d

# Stop Qdrant
docker-compose down

# Process data
python scripts/process_and_index.py --csv data/raw/CAvideos.csv

# Run interactive mode
python -m src.main

# Run single query
python -m src.main --query "Your question"

# Show system info
python -m src.main --info

# Run tests
pytest tests/test_multi_agent_system.py -v

# View logs
tail -f logs/youtube_trends_*.log

# Check Qdrant status
curl http://localhost:6333

# Restart everything
docker-compose restart
```

## ✅ Final Verification

Run this comprehensive test:

```bash
# 1. Check environment
python --version
docker --version

# 2. Check dependencies
pip list | grep -E "langchain|langgraph|qdrant"

# 3. Check databases
ls youtube_trends_canada.db
curl http://localhost:6333/collections

# 4. Run test query
python -m src.main --query "How many videos are there?"

# 5. Check logs
tail -n 20 logs/youtube_trends_*.log
```

If all steps pass: **🎉 Your multi-agent system is ready!**

## 📚 Next Steps

Once setup is complete:

1. **Explore the system**
   - Try different query types
   - Experiment with phrasing
   - Check which agents are used

2. **Read documentation**
   - [QUICKSTART_MULTI_AGENT.md](QUICKSTART_MULTI_AGENT.md)
   - [MULTI_AGENT_SETUP.md](MULTI_AGENT_SETUP.md)
   - [README_MULTI_AGENT.md](README_MULTI_AGENT.md)

3. **Run examples**
   ```bash
   python examples/multi_agent_example.py
   ```

4. **Customize**
   - Adjust settings in `.env`
   - Try different LLM models
   - Add more data sources

## 🆘 Getting Help

If you encounter issues:

1. Check this checklist again
2. Review error messages in logs
3. Consult [MULTI_AGENT_SETUP.md](MULTI_AGENT_SETUP.md) troubleshooting section
4. Run tests: `pytest tests/ -v`
5. Check Docker logs: `docker-compose logs`

---

**Happy analyzing! 🚀**
