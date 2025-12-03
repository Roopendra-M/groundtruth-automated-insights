import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Divider
} from '@mui/material';
import { Send, SmartToy } from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function ChatBot({ reportData }) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'Hello! I\'m your analytics assistant. Ask me anything about the report!'
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage = { type: 'user', text: question };
    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setLoading(true);

    try {
      // Get chatbot context from report data
      const context = reportData.chatbot_format || {
        kpis: reportData.kpis || [],
        insights: reportData.insights || [],
        summary: reportData.executive_summary || '',
        recommendations: reportData.business_recommendations || [],
        anomalies: reportData.anomaly_detection || '',
        trend_analysis: reportData.trend_analysis || ''
      };

      const response = await axios.post(`${API_BASE_URL}/chat`, {
        question: userMessage.text,
        context: context
      });

      setMessages(prev => [...prev, {
        type: 'bot',
        text: response.data.answer
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <SmartToy /> Chat with Analytics Assistant
      </Typography>

      <Paper sx={{ height: '500px', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          <List>
            {messages.map((msg, index) => (
              <React.Fragment key={index}>
                <ListItem
                  sx={{
                    justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
                    mb: 1
                  }}
                >
                  <Paper
                    sx={{
                      p: 2,
                      maxWidth: '70%',
                      bgcolor: msg.type === 'user' ? 'primary.main' : 'grey.200',
                      color: msg.type === 'user' ? 'white' : 'text.primary'
                    }}
                  >
                    <ListItemText
                      primary={msg.text}
                      primaryTypographyProps={{
                        style: { whiteSpace: 'pre-wrap' }
                      }}
                    />
                  </Paper>
                </ListItem>
                {index < messages.length - 1 && <Divider />}
              </React.Fragment>
            ))}
            {loading && (
              <ListItem>
                <CircularProgress size={24} />
              </ListItem>
            )}
          </List>
        </Box>

        <Divider />
        <Box sx={{ p: 2, display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask a question about the report..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <Button
            variant="contained"
            onClick={handleSend}
            disabled={loading || !question.trim()}
            startIcon={<Send />}
          >
            Send
          </Button>
        </Box>
      </Paper>

      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="text.secondary">
          <strong>Suggested questions:</strong>
        </Typography>
        <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {[
            'What are the top KPIs?',
            'What insights should I focus on?',
            'What are the main recommendations?',
            'Are there any anomalies in the data?'
          ].map((suggestion, index) => (
            <Button
              key={index}
              variant="outlined"
              size="small"
              onClick={() => setQuestion(suggestion)}
              disabled={loading}
            >
              {suggestion}
            </Button>
          ))}
        </Box>
      </Box>
    </Box>
  );
}

export default ChatBot;

