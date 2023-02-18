const express = require("express");
const mongoose = require("mongoose");
const User = require("./model/models");

//I nitialize express app
const app = express();

// parse application/x-www-form-urlencoded

// Connecting to DB
mongoose
  .connect(
    "mongodb://127.0.0.1:27017/myDB"
  )
  .then(() => app.listen(3000))
  .then(() =>
    console.log("Connected TO Database and Listening TO Localhost 3000")
  )
  .catch((err) => console.log(err));

  const bodyParser = require("body-parser")
  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(express.json());
// Reading a User from database

app.get("/:empId", async(req, res) => {
	const user = await User.findOne({
		empId: req.params.empId
	});
    res.send(user);
});

// Adding a User to AddressBook
app.post("/", (req, res) => {
  let newUser = new User({
	empId: req.body.empId,
    name: req.body.name,
    email: req.body.email,
    phone: req.body.phone,
    place: req.body.place,
  });
  console.log(newUser);
  newUser
    .save()
    .then((newUser) => {
      res.send(newUser);
    })
    .catch((err) => {
      console.log(err);
    });
});

// Updating the User

app.post("/update/:empId/editmail/:email", (req, res) => {
  let user = {};
  // if (req.body.empId) user.empId = req.body.empId;
  // if (req.body.name) user.name = req.body.name;
  if (req.params.email) user.email = req.params.email;
  // if (req.body.phone) user.phone = req.body.phone;
  // if (req.body.place) user.place = req.body.place;

  user = { $set: user };

  User.updateOne({ empId: req.params.empId }, user)
    .then(() => {
      
      res.send(user);
    })
    .catch((err) => {
      console.log(error);
    });
});

// Deleting the User from AddressBook

app.delete("/delete/:empId", (req, res) => {
  User.deleteOne({empId: req.params.empId })
    .then(() => {
      res.send("user deleted");
    })	
    .catch((err) => {
      console.log(err);
    });
});