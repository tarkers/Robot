import React from 'react'
import { ReactComponent as Eye } from '../img/eye.svg'
import { ReactComponent as Beard } from '../img/beard.svg'
import styled from "styled-components";
import { useSpring, animated } from 'react-spring'
const Mustache = styled(Beard)`
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color:#8a5c27;
`;
const RobotFace = () => {
    const showUp = useSpring({
        from: { opacity: 0 },
        to: { opacity: 1 },
        config: { duration: 1000 },
    })
    return (
        <animated.div style={showUp}>
            <div className="w-100 h-100" style={{ position: "fixed", zIndex: 1, backgroundColor: "#dbaf75",  }}>
                <div className="row" style={{ marginTop: "10%" }}>
                    <div className="col-4">
                        <div style={{ float: "right", marginTop: "1%" }}>
                            <Eye style={{ height: '400px' }}></Eye>
                        </div>
                    </div>
                    <div className="col-4" >
                        <div className="mx-auto" style={{ marginTop: "40%" }}>
                            <Beard style={{ height: '600px' }}></Beard>
                        </div>
                    </div>
                    <div className="col-4">
                        <div style={{ float: "left", marginTop: "1%" }}>
                            <Eye style={{ height: '400px' }}></Eye>
                        </div>
                    </div>
                </div>

            </div>
        </animated.div>
    )
}

export default RobotFace
