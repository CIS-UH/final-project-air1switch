const express = require("express");
const axios = require("axios");
const bodyParser = require("body-parser");
const app = express();
app.set("view engine", "ejs");

app.use(bodyParser.urlencoded({ extended: true }));

const API = "http://127.0.0.1:5000";

// index
app.get("/", (req, res) => {
    res.render("index");
});

// member page
app.get("/members", async (req, res) => {
    const response = await axios.get(`${API}/members`);
    res.render("members", { members: response.data });
});

// creating a member
app.post("/members", async (req, res) => {
    await axios.post(`${API}/members`, req.body);
    res.redirect("/members");
});

// deleting a member
app.post("/members/delete", async (req, res) => {
    await axios.delete(`${API}/members/${req.body.id}`);
    res.redirect("/members");
});


// event page
app.get("/events", async (req, res) => {
    const response = await axios.get(`${API}/events`);
    res.render("events", { events: response.data });
});

// creating an event
app.post("/events", async (req, res) => {
    await axios.post(`${API}/events`, req.body);
    res.redirect("/events");
});

// deleting an event
app.post("/events/delete", async (req, res) => {
    await axios.delete(`${API}/events/${req.body.id}`);
    res.redirect("/events");
});


// registration page
app.get("/registrations", async (req, res) => {
    const members = await axios.get(`${API}/members`);
    const events = await axios.get(`${API}/events`);
    const registrations = await axios.get(`${API}/registrations`);

    res.render("registrations", {
        members: members.data,
        events: events.data,
        registrations: registrations.data
    });
});

// creating a registration
app.post("/registrations", async (req, res) => {
    await axios.post(`${API}/registrations`, {
        memberId: req.body.memberId,
        eventId: req.body.eventId
    });
    res.redirect("/registrations");
});

// deleting registration
app.post("/registrations/delete", async (req, res) => {
    await axios.delete(`${API}/registrations/${req.body.id}`);
    res.redirect("/registrations");
});


app.listen(8081, () => {
    console.log("Page running at localhost:8081");
});