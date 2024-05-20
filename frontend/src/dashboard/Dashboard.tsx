import axios from "axios";
import React, { useEffect, useState } from "react";
import { BarChart } from "@mui/x-charts";
import { Alert, ToggleButton } from "react-bootstrap";
import { DatePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { useLoaderData } from "react-router-dom";
import "./Dashboard.css"

export default function Dashboard() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const graphTypes = [
        {id: "day", display: "Ngày"},
        {id: "week", display: "Tuần"},
        {id: "month", display: "Tháng"},
    ];

    const preloadData: any = useLoaderData();
    const [trafficGraphType, setTrafficGraphType] = useState(graphTypes[0].id);
    const [date, setDate] = useState(dayjs());
    const [cameraList, setCameraList] = useState<any>(preloadData.camera);
    const [trafficGraphCamera, setTrafficGraphCamera] = useState(preloadData.camera[0].id)
    const [allTrafficGraphData, setAllTrafficGraphData] = useState<any>(preloadData.traffic);
    const [trafficGraphData, setTrafficGraphData] = useState<any>(preloadData.traffic[trafficGraphCamera][trafficGraphType]);
    const [allAverageTrafficGraphData, setAllAverageTrafficGraphData] = useState<any>(preloadData.averageTraffic);
    const [averageTrafficGraphData, setAverageTrafficGraphData] = useState<any>(preloadData.averageTraffic[trafficGraphCamera][trafficGraphType]);
    const [allTotalTrafficGraphData, setAllTotalTrafficGraphData] = useState<any>(preloadData.totalTraffic);
    const [totalTrafficGraphData, setTotalTrafficGraphData] = useState<any>(preloadData.totalTraffic[trafficGraphType]);
    const [allAverageTotalTrafficGraphData, setAllAverageTotalTrafficGraphData] = useState<any>(preloadData.averageTotalTraffic);
    const [averageTotalTrafficGraphData, setAverageTotalTrafficGraphData] = useState<any>(preloadData.averageTotalTraffic[trafficGraphType])
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("");
    useEffect(() => {
        axios.get(apiUrl + "api/traffic", {params: {date: date.unix()}})
        .then((value) => {
            setAllTrafficGraphData(value.data);
            setTrafficGraphData(value.data[trafficGraphCamera][trafficGraphType] ?? [[0],[0]]);
        }).catch((reason) => {
            setError("Failed to fetch graph data");
            setShowAlert(true);
        })
        axios.get(apiUrl + "api/total-traffic", {params: {date: date.unix()}})
        .then((value) => {
            setAllTotalTrafficGraphData(value.data);
            setTotalTrafficGraphData(value.data[trafficGraphType] ?? [[0],[0]]);
        }).catch((reason) => {
            setError("Failed to fetch graph data");
            setShowAlert(true);
        })
        /*
        axios.get(apiUrl + "api/camera/")
        .then((value) => {
            setCameraList(value.data);
        }).catch((reason) => {
            setError(reason.toString());
            setShowAlert(true);
        })
        */
    }, [date]);

    return (
        <div className="h-100 overflow-hidden">
            <Alert className="m-3" show={showAlert} variant="danger" onClose={() => setShowAlert(false)} dismissible>
                {error}
            </Alert>
            <div className="row">
                <div className="ms-5 mt-5 vstack gap-3 col-2">
                    <DatePicker value={date} onChange={(event) => setDate(event ?? dayjs())}/>
                    <select className="p-2 bg-white rounded" value={trafficGraphCamera} onChange={(event) => {
                        setTrafficGraphCamera(event.target.value)
                        setTrafficGraphData(allTrafficGraphData[event.target.value][trafficGraphType] ?? [[0],[0]])
                        setAverageTrafficGraphData(allAverageTrafficGraphData[event.target.value][trafficGraphType])
                    }}>
                        {cameraList.map((value: any) => <option key={value.id} value={value.id}>{value.name}</option>)}
                    </select>
                    {graphTypes.map((value, index) => (
                        <ToggleButton variant="outline-secondary"
                        key={index} id={value.id} type="radio" 
                        value={value.id} checked={trafficGraphType === value.id} 
                        onChange={(e) => {
                            setTrafficGraphType(e.target.value)
                            setTrafficGraphData(allTrafficGraphData[trafficGraphCamera][e.target.value])
                            setAverageTrafficGraphData(allAverageTrafficGraphData[trafficGraphCamera][e.target.value])
                            setTotalTrafficGraphData(allTotalTrafficGraphData[e.target.value])
                            //setAverageTotalTrafficGraphData(allAverageTotalTrafficGraphData[e.target.value])
                        }}>
                            {value.display}
                        </ToggleButton>
                        ))}
                </div>
                <div className="col-9 d-flex flex-column align-item-center graph">
                    <label className="text-center fw-bold fs-3 mt-3">
                        Biểu đồ lượt khách ra vào
                    </label>
                    <div style={{minHeight: "40vh"}}>
                    <BarChart
                        series={[{data: trafficGraphData[0], label: "Lượt vào"}, {data: trafficGraphData[1], label: "Lượt ra"}]}/>
                    </div>
                    <label className="text-center fw-bold fs-3">
                        Biểu đồ lượt khách ra vào trung bình
                    </label>
                    <div style={{minHeight: "40vh"}}>
                    <BarChart
                        series={[{data: averageTrafficGraphData[0], label: "Lượt vào"}, {data: averageTrafficGraphData[1], label: "Lượt ra"}]}/>
                    </div>
                    <label className="text-center fw-bold fs-3">
                        Biểu đồ tổng lượt khách ra vào
                    </label>
                    <div style={{minHeight: "40vh"}}>
                    <BarChart
                        xAxis={[{ scaleType: 'band', data: allTotalTrafficGraphData.label}]}
                        series={[{data: totalTrafficGraphData[0], label: "Lượt vào"}, {data: totalTrafficGraphData[1], label: "Lượt ra"}]}/>
                    </div>
                    <label className="text-center fw-bold fs-3">
                        Biểu đồ tổng lượt khách ra vào trung bình
                    </label>
                    <div style={{minHeight: "40vh"}}>
                    <BarChart
                        xAxis={[{ scaleType: 'band', data: allAverageTotalTrafficGraphData.label}]}
                        series={[{data: averageTotalTrafficGraphData[0], label: "Lượt vào"}, {data: averageTotalTrafficGraphData[1], label: "Lượt ra"}]}/>
                    </div>
                </div>
                
            </div>
        </div>
    );
}