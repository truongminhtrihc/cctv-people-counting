import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { Navigate, RouterProvider, createBrowserRouter, redirect } from 'react-router-dom';
import reportWebVitals from './reportWebVitals';
import Dashboard from './dashboard/Dashboard';
import Header from './header/Header';
import Livestream from './livestream/Livestream';
import Vod from './vod/Vod';


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
      },
      {
        path: "/livestream",
        element: <Livestream/>,
      },
      {
        path: "/vod",
        element: <Vod/>,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
