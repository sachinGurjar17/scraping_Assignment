require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const { exec } = require('child_process');

const app = express();
const port = process.env.PORT || 5000;

mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch((err) => console.error('MongoDB connection error:', err));


const trendSchema = new mongoose.Schema({
    unique_id: String,
    trend1: String,
    trend2: String,
    trend3: String,
    trend4: String,
    trend5: String,
    date_time: Date,
    ip_address: String,
});
const Trend = mongoose.model('Trend', trendSchema);

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html'); 
});


app.post('/run-script', async (req, res) => {
    try {
        exec('python selenium_script.py', async (error, stdout, stderr) => {
            if (error) {
                console.error(`Script error: ${stderr}`);
                return res.status(500).json({ success: false, message: stderr });
            }

            const latestTrend = await Trend.findOne().sort({ date_time: -1 });

            if (!latestTrend) {
                return res.status(404).json({ success: false, message: 'No trends found.' });
            }

            res.json({
                success: true,
                trends: [latestTrend.trend1, latestTrend.trend2, latestTrend.trend3, latestTrend.trend4, latestTrend.trend5],
                unique_id: latestTrend.unique_id,
                ip_address: latestTrend.ip_address,
                date_time: latestTrend.date_time.toISOString(),
            });
        });
    } catch (err) {
        console.error('Error:', err);
        res.status(500).json({ success: false, message: 'Internal server error.' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
