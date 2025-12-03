import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip
} from '@mui/material';
import { ExpandMore, PictureAsPdf, Assessment } from '@mui/icons-material';

function ReportViewer({ reportData, onExportPDF }) {
  const [expanded, setExpanded] = useState('panel1');

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h2">
          Analytics Report
        </Typography>
        <Button
          variant="contained"
          startIcon={<PictureAsPdf />}
          onClick={onExportPDF}
          sx={{ bgcolor: '#d32f2f', '&:hover': { bgcolor: '#b71c1c' } }}
        >
          Export PDF
        </Button>
      </Box>

      {/* Executive Summary */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Assessment /> Executive Summary
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Typography variant="body1" paragraph>
            {reportData.executive_summary || 'No executive summary available.'}
          </Typography>
        </CardContent>
      </Card>

      {/* KPIs */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>Key Performance Indicators</Typography>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2}>
            {reportData.kpis && reportData.kpis.map((kpi, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Chip
                  label={kpi}
                  color="primary"
                  sx={{ width: '100%', height: 'auto', py: 2, '& .MuiChip-label': { whiteSpace: 'normal' } }}
                />
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Expandable Sections */}
      <Accordion expanded={expanded === 'panel1'} onChange={handleChange('panel1')}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">Data Understanding</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
            {reportData.data_understanding || 'No data understanding available.'}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'panel2'} onChange={handleChange('panel2')}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">Trend Analysis</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
            {reportData.trend_analysis || 'No trend analysis available.'}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'panel3'} onChange={handleChange('panel3')}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">Anomaly Detection</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
            {reportData.anomaly_detection || 'No anomalies detected.'}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'panel4'} onChange={handleChange('panel4')}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">Correlation Analysis</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
            {reportData.correlation_analysis || 'No correlation analysis available.'}
          </Typography>
        </AccordionDetails>
      </Accordion>

      {/* Insights */}
      <Card sx={{ mt: 3, mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>Key Insights</Typography>
          <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.3)' }} />
          <List>
            {reportData.insights && reportData.insights.map((insight, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={insight}
                  primaryTypographyProps={{ style: { color: 'white' } }}
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Recommendations */}
      <Card sx={{ mb: 3, bgcolor: 'success.light', color: 'success.contrastText' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>Business Recommendations</Typography>
          <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.3)' }} />
          <List>
            {reportData.business_recommendations && reportData.business_recommendations.map((rec, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={`${index + 1}. ${rec}`}
                  primaryTypographyProps={{ style: { color: 'white' } }}
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Slide Deck Preview */}
      {reportData.slide_deck && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>Slide Deck Content</Typography>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6" gutterBottom>Slide 1: Title</Typography>
            <Typography variant="body2" paragraph>
              {reportData.slide_deck.slide_1_title || 'N/A'}
            </Typography>
            <Typography variant="h6" gutterBottom>Slide 7: Final Summary</Typography>
            <Typography variant="body2">
              {reportData.slide_deck.slide_7_summary || 'N/A'}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default ReportViewer;

