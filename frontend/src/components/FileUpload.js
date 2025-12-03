import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

function FileUpload({ onFileUpload, loading }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onFileUpload(acceptedFiles[0]);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    multiple: false
  });

  return (
    <Box>
      <Paper
        {...getRootProps()}
        sx={{
          p: 6,
          textAlign: 'center',
          cursor: 'pointer',
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'action.hover'
          }
        }}
      >
        <input {...getInputProps()} />
        {loading ? (
          <Box>
            <CircularProgress size={60} sx={{ mb: 2 }} />
            <Typography variant="h6">Processing your file...</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Analyzing data and generating report
            </Typography>
          </Box>
        ) : (
          <Box>
            <CloudUpload sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              {isDragActive ? 'Drop your CSV file here' : 'Upload CSV File'}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
              Drag and drop a CSV file, or click to select
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              Supported format: CSV files only
            </Typography>
          </Box>
        )}
      </Paper>
    </Box>
  );
}

export default FileUpload;

