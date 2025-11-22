import React, { useState } from 'react';
import FileUpload from './FileUpload';
import History from './History';
import Charts from './Charts';

const Dashboard = ({ auth }) => {
    const [currentUploadId, setCurrentUploadId] = useState(null);
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    const handleUploadSuccess = (id) => {
        setRefreshTrigger(prev => prev + 1);
        setCurrentUploadId(id);
    };

    return (
        <div className="min-h-screen p-8 bg-gray-100">
            <h1 className="mb-8 text-3xl font-bold text-center text-gray-800">Chemical Equipment Visualizer</h1>

            <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
                <div className="md:col-span-1">
                    <FileUpload onUploadSuccess={handleUploadSuccess} auth={auth} />
                    <History
                        onSelectUpload={setCurrentUploadId}
                        refreshTrigger={refreshTrigger}
                        auth={auth}
                    />
                </div>

                <div className="md:col-span-2">
                    <Charts uploadId={currentUploadId} auth={auth} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
