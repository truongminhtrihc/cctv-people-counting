import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import axios from 'axios';
// Định nghĩa kiểu dữ liệu cho các props
interface YourEditFormProps {
  cameraId: number;
  currentName: string;
  onClose: () => void; // Hàm không nhận tham số và không trả về gì
}

// Sử dụng kiểu dữ liệu đã định nghĩa
const YourEditForm: React.FC<YourEditFormProps> = ({ cameraId, currentName, onClose }) => {
  const [newName, setNewName] = React.useState(currentName);

  const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNewName(event.target.value);
  };

  const handleCancel = () => {
    onClose();
  };

  const handleSave = () => {
    // Gọi API để lưu tên mới
    axios.post('http://localhost:8000/api/camera/change-name/', {
      id: cameraId,
      name: newName
    })
    .then(response => {
      console.log(response.data); // Log kết quả trả về từ API
      onClose(); // Đóng form sau khi lưu thành công
    })
    .catch(error => {
      console.error('Error:', error); // Log lỗi nếu có
      // Xử lý lỗi hoặc hiển thị thông báo cho người dùng nếu cần
    });
  };
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(0, 0, 0, 0.7)', /* Màu đen với độ trong suốt 50% */
      zIndex: 999,
    }}>
      <Box
        sx={{ 
          width: '30rem',
          height:'16rem',
          display: 'flex', 
          flexDirection: 'column', 
          justifyContent: 'center',
          gap: 2, 
          backgroundColor: 'white', 
          padding: '20px', 
          borderRadius: '8px',
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 9999, // Đảm bảo form được hiển thị trên tất cả các phần tử khác trên trang
        }}
      >
        <TextField
          label="New Camera Name"
          variant="outlined"
          value={newName}
          onChange={handleNameChange}
        />
        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button variant="outlined" onClick={handleCancel}>
            Cancel
          </Button>
          <Button variant="contained" onClick={handleSave} sx={{marginLeft:'2rem'}}>
            Save
          </Button>
        </Box>
      </Box>
    </div>
  );
};

export default YourEditForm;
