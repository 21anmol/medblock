import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = ({ user }) => {
  const [healthPrediction, setHealthPrediction] = useState(null);
  const [anomalyStats, setAnomalyStats] = useState(null);
  const [fraudStats, setFraudStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from API
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get healthcare prediction
        if (user.role === 'patient') {
          const healthResponse = await axios.post('http://localhost:5000/api/healthcare/predict', {
            age: user.age,
            gender: user.gender,
            bmi: user.bmi || 25,
            systolic_bp: user.systolic_bp || 120,
            diastolic_bp: user.diastolic_bp || 80,
            heart_rate: user.heart_rate || 75,
            glucose: user.glucose || 90,
            cholesterol: user.cholesterol || 180,
          });
          setHealthPrediction(healthResponse.data);
        }
        
        // Get anomaly statistics
        if (user.role === 'admin' || user.role === 'provider') {
          const anomalyResponse = await axios.get('http://localhost:5000/api/access/stats');
          setAnomalyStats(anomalyResponse.data);
        }
        
        // Get fraud statistics
        if (user.role === 'admin' || user.role === 'insurance') {
          const fraudResponse = await axios.get('http://localhost:5000/api/fraud/stats');
          setFraudStats(fraudResponse.data);
        }
        
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  // Chart data for anomalies
  const anomalyChartData = {
    labels: ['Normal Access', 'Anomalous Access'],
    datasets: [
      {
        data: anomalyStats ? [anomalyStats.normal_count, anomalyStats.anomaly_count] : [95, 5],
        backgroundColor: ['#4ade80', '#f87171'],
        borderColor: ['#16a34a', '#dc2626'],
        borderWidth: 1,
      },
    ],
  };

  // Chart data for fraud
  const fraudChartData = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk'],
    datasets: [
      {
        label: 'Risk Level Distribution',
        data: fraudStats ? [fraudStats.low_risk, fraudStats.medium_risk, fraudStats.high_risk] : [70, 20, 10],
        backgroundColor: ['#4ade80', '#facc15', '#f87171'],
      },
    ],
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>
      
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Health Prediction Card */}
          {user.role === 'patient' && healthPrediction && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-700 mb-4">Health Prediction</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Risk Level:</span>
                  <span className={`font-medium ${healthPrediction.risk_level === 'Low' ? 'text-green-600' : healthPrediction.risk_level === 'Medium' ? 'text-yellow-600' : 'text-red-600'}`}>
                    {healthPrediction.risk_level}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Confidence:</span>
                  <span className="font-medium">{Math.round(healthPrediction.confidence * 100)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className={`h-2.5 rounded-full ${healthPrediction.risk_level === 'Low' ? 'bg-green-600' : healthPrediction.risk_level === 'Medium' ? 'bg-yellow-500' : 'bg-red-600'}`}
                    style={{ width: `${Math.round(healthPrediction.confidence * 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}
          
          {/* Anomaly Detection Card */}
          {(user.role === 'admin' || user.role === 'provider') && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-700 mb-4">Access Pattern Analysis</h2>
              <div className="h-64">
                <Pie data={anomalyChartData} options={{ maintainAspectRatio: false }} />
              </div>
              {anomalyStats && (
                <div className="mt-4 text-sm text-gray-600">
                  <p>Total access attempts: {anomalyStats.total_count}</p>
                  <p>Anomalies detected: {anomalyStats.anomaly_count} ({(anomalyStats.anomaly_count / anomalyStats.total_count * 100).toFixed(1)}%)</p>
                </div>
              )}
            </div>
          )}
          
          {/* Fraud Detection Card */}
          {(user.role === 'admin' || user.role === 'insurance') && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-700 mb-4">Fraud Risk Distribution</h2>
              <div className="h-64">
                <Bar
                  data={fraudChartData}
                  options={{
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true
                      }
                    }
                  }}
                />
              </div>
              {fraudStats && (
                <div className="mt-4 text-sm text-gray-600">
                  <p>Total claims analyzed: {fraudStats.total_claims}</p>
                  <p>High risk claims: {fraudStats.high_risk} ({(fraudStats.high_risk / fraudStats.total_claims * 100).toFixed(1)}%)</p>
                </div>
              )}
            </div>
          )}
          
          {/* Recent Activity Card */}
          <div className="bg-white p-6 rounded-lg shadow-md lg:col-span-3">
            <h2 className="text-xl font-semibold text-gray-700 mb-4">Recent Activity</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left text-gray-500">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                  <tr>
                    <th className="px-6 py-3">Time</th>
                    <th className="px-6 py-3">Activity</th>
                    <th className="px-6 py-3">Status</th>
                    <th className="px-6 py-3">Details</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Sample activities - these would come from API in a real implementation */}
                  <tr className="bg-white border-b">
                    <td className="px-6 py-4">2023-03-15 09:30</td>
                    <td className="px-6 py-4">Medical Record Access</td>
                    <td className="px-6 py-4"><span className="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded">Approved</span></td>
                    <td className="px-6 py-4">Dr. Smith accessed Patient #12345's records</td>
                  </tr>
                  <tr className="bg-white border-b">
                    <td className="px-6 py-4">2023-03-14 14:45</td>
                    <td className="px-6 py-4">Insurance Claim</td>
                    <td className="px-6 py-4"><span className="bg-yellow-100 text-yellow-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded">Pending</span></td>
                    <td className="px-6 py-4">Claim #78901 submitted for review</td>
                  </tr>
                  <tr className="bg-white">
                    <td className="px-6 py-4">2023-03-13 23:15</td>
                    <td className="px-6 py-4">Unauthorized Access Attempt</td>
                    <td className="px-6 py-4"><span className="bg-red-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded">Blocked</span></td>
                    <td className="px-6 py-4">Unknown IP attempted to access Patient #34567's records</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 