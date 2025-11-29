import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  TrendingUp,
  Eye,
  ThumbsUp,
  MessageCircle,
  Calendar,
  Tag,
  Sparkles,
  Database,
  Zap,
  Clock,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Badge } from './ui/Badge';

export function ResultsDisplay({ response }) {
  if (!response) return null;

  const { answer, metadata, results, processing_time } = response;

  const getAgentIcon = (agentType) => {
    switch (agentType) {
      case 'sql':
        return <Database className="h-4 w-4" />;
      case 'vector':
        return <Sparkles className="h-4 w-4" />;
      case 'hybrid':
        return <Zap className="h-4 w-4" />;
      default:
        return <Sparkles className="h-4 w-4" />;
    }
  };

  const getAgentColor = (agentType) => {
    switch (agentType) {
      case 'sql':
        return 'default';
      case 'vector':
        return 'secondary';
      case 'hybrid':
        return 'success';
      default:
        return 'outline';
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num?.toLocaleString() || '0';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-6xl mx-auto space-y-6"
    >
      {/* Metadata Bar */}
      {metadata && (
        <div className="flex flex-wrap items-center gap-3 p-4 bg-muted/50 rounded-lg border">
          {metadata.query_type && (
            <Badge variant={getAgentColor(metadata.query_type)}>
              {getAgentIcon(metadata.query_type)}
              <span className="ml-1.5 capitalize">{metadata.query_type}</span>
            </Badge>
          )}
          {metadata.agents_used && metadata.agents_used.length > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground">Agents:</span>
              {metadata.agents_used.map((agent, idx) => (
                <Badge key={idx} variant="outline" className="text-xs">
                  {agent}
                </Badge>
              ))}
            </div>
          )}
          {metadata.confidence !== undefined && (
            <Badge variant="outline">
              <TrendingUp className="h-3 w-3 mr-1" />
              {(metadata.confidence * 100).toFixed(0)}% Confidence
            </Badge>
          )}
          {processing_time && (
            <Badge variant="outline">
              <Clock className="h-3 w-3 mr-1" />
              {processing_time.toFixed(2)}s
            </Badge>
          )}
        </div>
      )}

      {/* Answer Section */}
      <Card className="shadow-sm youtube-card-hover">
        <CardHeader className="border-b">
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <span>Answer</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {answer}
            </ReactMarkdown>
          </div>
        </CardContent>
      </Card>

      {/* Results Grid */}
      {results && results.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            Detailed Results ({results.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.map((result, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <VideoCard result={result} index={index} />
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

function VideoCard({ result, index }) {
  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num?.toLocaleString() || '0';
  };

  return (
    <Card className="hover:shadow-lg transition-shadow duration-200 h-full">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base line-clamp-2 flex-1">
            {result.title || 'Untitled Video'}
          </CardTitle>
          {result.score !== undefined && (
            <Badge variant="secondary" className="flex-shrink-0">
              {(result.score * 100).toFixed(0)}%
            </Badge>
          )}
        </div>
        {result.channel_title && (
          <p className="text-sm text-muted-foreground">
            {result.channel_title}
          </p>
        )}
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Stats */}
        <div className="grid grid-cols-2 gap-2">
          {result.views !== undefined && (
            <div className="flex items-center gap-1.5 text-sm">
              <Eye className="h-4 w-4 text-muted-foreground" />
              <span className="font-medium">{formatNumber(result.views)}</span>
              <span className="text-muted-foreground text-xs">views</span>
            </div>
          )}
          {result.likes !== undefined && (
            <div className="flex items-center gap-1.5 text-sm">
              <ThumbsUp className="h-4 w-4 text-muted-foreground" />
              <span className="font-medium">{formatNumber(result.likes)}</span>
              <span className="text-muted-foreground text-xs">likes</span>
            </div>
          )}
          {result.comment_count !== undefined && (
            <div className="flex items-center gap-1.5 text-sm">
              <MessageCircle className="h-4 w-4 text-muted-foreground" />
              <span className="font-medium">
                {formatNumber(result.comment_count)}
              </span>
              <span className="text-muted-foreground text-xs">comments</span>
            </div>
          )}
          {result.trending_date && (
            <div className="flex items-center gap-1.5 text-sm">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground text-xs">
                {result.trending_date}
              </span>
            </div>
          )}
        </div>

        {/* Category & Tags */}
        <div className="flex flex-wrap gap-2">
          {result.category && (
            <Badge variant="outline" className="text-xs">
              <Tag className="h-3 w-3 mr-1" />
              {result.category}
            </Badge>
          )}
          {result.tags && result.tags.length > 0 && (
            <>
              {result.tags.slice(0, 2).map((tag, idx) => (
                <Badge key={idx} variant="secondary" className="text-xs">
                  {tag}
                </Badge>
              ))}
              {result.tags.length > 2 && (
                <Badge variant="secondary" className="text-xs">
                  +{result.tags.length - 2}
                </Badge>
              )}
            </>
          )}
        </div>

        {/* Description */}
        {result.description && (
          <p className="text-xs text-muted-foreground line-clamp-2">
            {result.description}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
