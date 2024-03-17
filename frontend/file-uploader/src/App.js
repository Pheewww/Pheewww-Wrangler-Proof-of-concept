import React, { useState } from 'react';
import axios from 'axios';
import { DataGrid } from '@mui/x-data-grid';
import { Button, TextField, Input } from '@mui/material';

const FileUploader = ({ onFileUpload }) => {
  return (
    <Button variant="outlined" component="label">
   
      <Input type="file" hidden onChange={onFileUpload} />
    </Button>
  );
};

const DataTable = ({ columns, rows }) => {
  return (
    <div style={{ height: 600, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
      />
    </div>
  );
};

const processDataForGrid = (data) => {
  const columns = data.length > 0 ? Object.keys(data[0]).map((key, index) => ({
    field: key,
    headerName: key.split('.').join(' '),
    width: 300,
  })) : [];

  const rows = data.map((row, index) => ({ id: index, ...row }));

  return { columns, rows };
};

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [datasetData, setDatasetData] = useState([]);
  const [filterCondition, setFilterCondition] = useState('');

  const handleFilter = async () => {
    if (!uploadedFile || !filterCondition) {
      alert('Please upload a file and enter a filter condition.');
      return;
    }

    const payload = {
      operation_type: 'filter',
      parameters: { filter_condition: filterCondition }
    };

    try {
      const response = await fetch(`http://localhost:8000/datasets/${uploadedFile.dataset_id}/transform`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
        return;
      }

      const data = await response.json();
      setDatasetData(data);

    } catch (error) {
      console.error('Error filtering dataset:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/datasets/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setUploadedFile({ filename: response.data.filename, file_path: response.data.file_path, dataset_id: response.data.dataset_id });
      setDatasetData(response.data.dataset);

    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const { columns, rows } = React.useMemo(() => processDataForGrid(datasetData), [datasetData]);

  return (
    <div className="App" style={{ margin: 20 }}>
      <h1>Upload File</h1>
      <FileUploader onFileUpload={handleFileUpload} />
      {uploadedFile && (
        <>
          <TextField
            label="Filter Condition"
            variant="outlined"
            placeholder="Enter filter condition, e.g., sepal_length > 4.5"
            value={filterCondition}
            onChange={(e) => setFilterCondition(e.target.value)}
          />
          <Button variant="contained" color="primary" onClick={handleFilter}>
            Apply Filter
          </Button>
          {datasetData.length > 0 && (
            <>
              <h2>Uploaded File: {uploadedFile.filename}</h2>
              <DataTable columns={columns} rows={rows} />
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;
