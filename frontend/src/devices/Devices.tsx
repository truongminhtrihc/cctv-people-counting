
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import EditIcon from '@mui/icons-material/Edit';
import React, { useState, useEffect,ChangeEvent } from 'react';
import axios from 'axios';

import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { styled, alpha } from '@mui/material/styles';   
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import InputBase from '@mui/material/InputBase';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import EditForm from './EditForm';

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: "#a0a0a0",
  '&:hover': {
    backgroundColor: "#dcdcdc",
  },    
  width: '100%',
  height: '3rem',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: '30rem',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  height: '3rem',
  fontSize: '1.6rem',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    [theme.breakpoints.up('sm')]: {
      width: '20rem',
      '&:focus': {
        width: '24rem',
      },
    },
  },
}));
interface Camera {
    id: number;
    name: string;
    status: string;
    type: string;
    video_ip: string;
    camera_ip: string;
  }
 
  interface Column {
    id: 'name' ;
    label: string;
    minWidth?: number;
    align?: 'right' | 'left';
    format?: (value: number) => string;
  }
  
  const columns: readonly Column[] = [
    { id: 'name', label: 'Danh sách các camera', minWidth: 200 },
  ];
  

  
export default function Devices() {
  const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
  const [cameras, setCameras] = useState<Camera[]>([]);

  useEffect(() => {
      const fetchCameras = async () => {
      try {
          const response = await axios.get<Camera[]>(apiUrl + 'api/camera/');
          setCameras(response.data);
      } catch (error) {
          console.error('Error fetching cameras:', error);
      }
      };

      fetchCameras();
  }, []);


  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };
  
  const [searchValue, setSearchValue] = useState('');
  
  const handleSearchChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchValue(event.target.value.toLowerCase())
  };

  const filteredCameras = searchValue === ''
    ? cameras
    : cameras.filter(camera =>
        camera.name.toLowerCase().includes(searchValue.toLowerCase())
      );


    const [editFormOpen, setEditFormOpen] = useState(false);
    

  
    const handleCloseForm = () => {
      setEditFormOpen(false); // Đóng form khi cần
    };

    const [selectedCameraId, setSelectedCameraId] = useState(0);
    const [selectedCameraName, setSelectedCameraName] = useState('');
    const handleEditClick = (cameraId:number, cameraName:string) => {
      setSelectedCameraId(cameraId);
      setSelectedCameraName(cameraName);
      setEditFormOpen(true);
    };
    return (

        <div>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Search 
            sx = {{
                margin: '2rem',
                display:'flex',
                alignItems: 'center',
            }}>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Tìm kiếm"
              inputProps={{ 'aria-label': 'search' }}
              value={searchValue}
              onChange={handleSearchChange}
            />
          </Search>
          </div>
           
            <Box
      
      my={4}
      display="flex"
      alignItems="center"
      gap={4}
      p={2}
      sx={{ border: '2px solid grey', width:"50rem", margin:"0 auto" }}
    >
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer >
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align="center"
                  style={{ minWidth: column.minWidth , fontSize: "1.5rem", backgroundColor:"blue", color: "white"}}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
          {filteredCameras.map((camera, index)=> (
  <TableRow hover role="checkbox" tabIndex={-1} key={index} >
    <TableCell align="center" >
      <Card sx={{ maxWidth: "60rem", display: 'flex', backgroundColor: '#3D5278' }}>
        <CardMedia
          component="img"
          alt="camera"
          image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2DAkmD4BVPixBzyy2lyvtF_Q2HPbrtgEd8pvoRujePA&s"
          sx={{ 
            width: '8rem', 
            height: '8rem', 
            objectFit: 'cover', 
            padding: '1rem',
            flex: '0 0 1',
            display: 'block',
            overflow: 'hidden' 
          }}
        />
        <CardContent style={{ textAlign: 'left', flex: '1' }}>
          <Typography gutterBottom variant="h5" component="div" color="white">
            {camera.name}
          </Typography>
          <Typography variant="body2" color="white">
            Dòng: Camera {camera.type === 'AREA'? 'Trong nhà' : 'Ngoài trời'}
          </Typography>
          <Typography variant="body2" color="white">
      Trạng thái: <span style={{ color: camera.status === 'ON' ? 'green' : camera.status === 'OFF' ? 'red' : 'brown' }}>
        {camera.status === 'ON' ? 'Hoạt động' : camera.status === 'OFF' ? 'Không hoạt động' : 'Không có kết nối'}
        </span> 
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="large" sx={{
            marginRight: '1rem',
            backgroundColor: 'white',
            '&:hover': {
              backgroundColor: '#dcdcdc'
            },
          }}
          onClick={() => handleEditClick(camera.id, camera.name)}>
            <EditIcon />
            Edit
          </Button>
        </CardActions>
      </Card>
    </TableCell>
  </TableRow>
))}

          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10]}
        component="div"
        count={cameras.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
    </Box>
    
    {editFormOpen && (
    <EditForm
      cameraId={selectedCameraId}
      currentName={selectedCameraName}
      onClose={handleCloseForm}
    />
  )}
        </div>
    )
}