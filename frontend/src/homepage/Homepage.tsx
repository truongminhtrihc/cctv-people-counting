import React from "react";
import "./Homepage.css"
import cam from "../assets/cam.png"
import cam1 from "../assets/cam1.png"
import { Carousel } from "react-bootstrap";
export default function Homepage() {
    return (
        <div className="text-center">
            <Carousel interval={2000}>
                <Carousel.Item>
                    <img
                        className="carousel-custom"
                        src={cam1}
                        alt="First slide"
                    />
                    <Carousel.Caption>
                        <h5>WELLCOME TO OUR WEBSITE!</h5>
                    </Carousel.Caption>
                </Carousel.Item>
                <Carousel.Item>
                    <img
                        className="carousel-custom"
                        src={cam}
                        alt="First slide"
                    />
                    <Carousel.Caption>
                        <h5>ARMED AND READY FOR YOUR SAFETY</h5>
                    </Carousel.Caption>
                </Carousel.Item>
            </Carousel>
        </div>
    )
}