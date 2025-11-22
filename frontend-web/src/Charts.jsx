import React, { useEffect, useState } from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import api from './api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Charts = ({ uploadId, auth }) => {
    const [data, setData] = useState(null);

    useEffect(() => {
        if (!uploadId) return;

        const fetchData = async () => {
            try {
                const response = await api.get(`summary/${uploadId}/`, {
                    headers: {
                        'Authorization': `Basic ${btoa(`${auth.username}:${auth.password}`)}`
                    }
                });
                setData(response.data);
            } catch (error) {
                console.error('Error fetching summary:', error);
            }
        };
        fetchData();
    }, [uploadId, auth]);

    if (!data) return <div className="p-4 text-center text-gray-500">Select an upload to view stats</div>;

    const barData = {
        labels: ['Average Flowrate', 'Average Pressure', 'Average Temperature'],
        datasets: [
            {
                label: 'Averages',
                data: [data.avg_flowrate, data.avg_pressure, data.avg_temperature],
                backgroundColor: ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)'],
                borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
                borderWidth: 1,
            },
        ],
    };

    const pieData = {
        labels: data.type_distribution.map(d => d.equipment_type),
        datasets: [
            {
                data: data.type_distribution.map(d => d.count),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    const handleDownloadPDF = () => {
        window.open(`http://localhost:8000/api/pdf/${uploadId}/`, '_blank');
    };

    return (
        <div className="p-4 bg-white rounded shadow">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Analysis for {data.filename}</h2>
                <button onClick={handleDownloadPDF} className="px-3 py-1 text-white bg-purple-500 rounded hover:bg-purple-700">
                    Download PDF
                </button>
            </div>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                    <h3 className="mb-2 text-lg font-semibold text-center">Parameter Averages</h3>
                    <Bar data={barData} />
                </div>
                <div>
                    <h3 className="mb-2 text-lg font-semibold text-center">Equipment Type Distribution</h3>
                    <div className="w-2/3 mx-auto">
                        <Pie data={pieData} />
                    </div>
                </div>
            </div>

            <div className="mt-4">
                <p><strong>Total Equipment Count:</strong> {data.total_count}</p>
            </div>
        </div>
    );
};

export default Charts;
