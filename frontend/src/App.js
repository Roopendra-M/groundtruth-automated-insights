import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import { CloudUpload, Assessment, Insights, Chat } from '@mui/icons-material';
import FileUpload from './components/FileUpload';
import ReportViewer from './components/ReportViewer';
import ChatBot from './components/ChatBot';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setReportData(response.data);
      setActiveTab(1); // Switch to report view
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/export/pdf`,
        reportData,
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `analytics_report_${new Date().toISOString().split('T')[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to export PDF. Please try again.');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ color: 'white', fontWeight: 'bold' }}>
          📊 AI Analytics Report Generator
        </Typography>
        <Typography variant="h6" sx={{ color: 'rgba(255,255,255,0.9)', mt: 1 }}>
          Upload your CSV dataset and get comprehensive weekly analytics reports
        </Typography>
      </Box>

      <Paper elevation={10} sx={{ p: 3, borderRadius: 3 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
          <Tab icon={<CloudUpload />} label="Upload" />
          <Tab icon={<Assessment />} label="Report" disabled={!reportData} />
          <Tab icon={<Chat />} label="Chat" disabled={!reportData} />
        </Tabs>

        {activeTab === 0 && (
          <FileUpload onFileUpload={handleFileUpload} loading={loading} />
        )}

        {activeTab === 1 && reportData && (
          <ReportViewer reportData={reportData} onExportPDF={handleExportPDF} />
        )}

        {activeTab === 2 && reportData && (
          <ChatBot reportData={reportData} />
        )}
      </Paper>
    </Container>
  );
}

export default App;

