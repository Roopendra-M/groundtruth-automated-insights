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

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

function ReportViewer({ reportData, onExportPDF, onExportPPTX }) {
  const [expanded, setExpanded] = useState('panel1');

  const safeText = (value) => {
    if (value === null || value === undefined) return "";
    if (typeof value === "string") return value;
    try {
      return JSON.stringify(value, null, 2);
    } catch {
      return String(value);
    }
  };

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
    };

  // Build chart-friendly KPI numbers
  const buildKpiChartData = () => {
    if (!reportData.kpis || !Array.isArray(reportData.kpis)) return [];
    return reportData.kpis.map((kpi, idx) => {
      const text = safeText(kpi);
      const match = text.match(/([-+]?\d*\.?\d+)/);
      return {
        name: text.split(':')[0].slice(0, 20) || `KPI ${idx + 1}`,
        value: match ? Number(match[1]) : 0
      };
    });
  };

  const kpiChartData = buildKpiChartData();

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Analytics Report</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="outlined" onClick={onExportPPTX}>Export PPTX</Button>
          <Button
            variant="contained"
            startIcon={<PictureAsPdf />}
            onClick={onExportPDF}
            sx={{ bgcolor: '#d32f2f', '&:hover': { bgcolor: '#b71c1c' } }}
          >
            Export PDF
          </Button>
        </Box>
      </Box>

      {/* Executive Summary */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Assessment /> Executive Summary
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Typography variant="body1" paragraph>
            {safeText(reportData.executive_summary)}
          </Typography>
        </CardContent>
      </Card>

      {/* KPI Section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5">Key Performance Indicators</Typography>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2}>
            {reportData.kpis && reportData.kpis.map((kpi, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Chip
                  label={safeText(kpi)}
                  color="primary"
                  sx={{ width: '100%', py: 2 }}
                />
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Charts */}
      {kpiChartData.length > 0 && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5">Charts & Visuals</Typography>
            <Divider sx={{ my: 2 }} />
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Basic visualization of numeric values extracted from KPIs.
            </Typography>

            <Box sx={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <BarChart data={kpiChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#1976d2" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Expand Sections */}
      {[
        { id: "panel1", title: "Data Understanding", value: reportData.data_understanding },
        { id: "panel2", title: "Trend Analysis", value: reportData.trend_analysis },
        { id: "panel3", title: "Anomaly Detection", value: reportData.anomaly_detection },
        { id: "panel4", title: "Correlation Analysis", value: reportData.correlation_analysis }
      ].map((section, idx) => (
        <Accordion expanded={expanded === section.id} onChange={handleChange(section.id)} key={idx}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">{section.title}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
              {safeText(section.value)}
            </Typography>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Insights */}
      <Card sx={{ mt: 3, mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <CardContent>
          <Typography variant="h5">Key Insights</Typography>
          <Divider sx={{ my: 2 }} />
          <List>
            {reportData.insights && reportData.insights.map((insight, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={safeText(insight)}
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
          <Typography variant="h5">Business Recommendations</Typography>
          <Divider sx={{ my: 2 }} />
          <List>
            {reportData.business_recommendations &&
              reportData.business_recommendations.map((rec, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`${index + 1}. ${safeText(rec)}`}
                    primaryTypographyProps={{ style: { color: 'white' } }}
                  />
                </ListItem>
              ))}
          </List>
        </CardContent>
      </Card>

      {/* Slide Deck */}
      {reportData.slide_deck && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5">Slide Deck Content</Typography>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6">Slide 1: Title</Typography>
            <Typography variant="body2" paragraph>{safeText(reportData.slide_deck.slide_1_title)}</Typography>

            <Typography variant="h6">Slide 7: Final Summary</Typography>
            <Typography variant="body2">{safeText(reportData.slide_deck.slide_7_summary)}</Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default ReportViewer;
