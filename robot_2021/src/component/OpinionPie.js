import React from 'react';
import { Pie } from 'react-chartjs-2';

const data = {
    labels: ['1', '2', '3', '4', '5'],
    datasets: [
        {
            label: '# opinion',
            data: [12, 19, 3, 5, 2],
            borderColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
            ],
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
            ],
            borderWidth: 5,
        },
    ],
};

const PieChart = () => (
    <>
        {/* <div className='header'>
      <h1 className='title'>Pie Chart</h1>
      <div className='links'>
        <a
          className='btn btn-gh'
          href='https://github.com/reactchartjs/react-chartjs-2/blob/master/example/src/charts/Pie.js'
        >
          Github Source
        </a>
      </div>
    </div> */}
        <div >
            <div className="text-center" style={{ width: "400px", height: "600px" }}>
                <h1>評價分數</h1>
                <Pie data={data} />
            </div>
        </div>


    </>
);

export default PieChart;