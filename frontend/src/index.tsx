import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import { Navigate, RouterProvider, createBrowserRouter } from 'react-router-dom';
import reportWebVitals from './reportWebVitals';
import Dashboard from './dashboard/Dashboard';
import Header from './header/Header';
import Livestream from './livestream/Livestream';
import Vod from './vod/Vod';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import 'dayjs/locale/vi';
import axios from 'axios';
import Devices from './devices/Devices';

const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Header/>,
    
    children: [
      {
        index: true,
        element: <Navigate replace to='/dashboard' />,
      },
      {
        path: "/dashboard",
        element: <Dashboard/>,
        loader: async ({request}) => {
          let camera, traffic;
          try {
            camera = (await axios.get(apiUrl + "api/camera/")).data;
          } catch (error: any) {
            camera = [{"id": -1, "name": "Can't fetch data"}];
          }
          try {
            traffic = (await axios.get(apiUrl + "api/traffic")).data
          } catch (error: any) {
            traffic = {"-1":[[0],[0]]}
          }
          return {
            camera: camera,
            traffic: traffic
          }
        }
      },
      {
        path: "/livestream",
        element: <Livestream/>,
        loader: async ({request}) => {
          let camera;
          try {
            camera = (await axios.get(apiUrl + "api/camera/")).data;
          } catch (error: any) {
            camera = [{"id": -1, "name": "Can't fetch data"}];
          }
          return {
            camera: camera
          }
        }
      },
      {
        path: "/vod",
        element: <Vod/>,
      },
      {
        path: "/devices",
        element: <Devices/>,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="vi">
      <RouterProvider router={router}/>
    </LocalizationProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
