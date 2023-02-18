const mongoose = require('mongoose')

// Schema for User
const userSchema = mongoose.Schema({
	empId: {
		type: Number,
		required: true
	},
	name: {
		type: String,
		required: true
	},
	email: {
		type: String,
		required: true
	},
	phone: {
		type: Number,
		required: true
	},
	place: {
		type: String,
		required: true
	}
})

//Creating the collection Address
const User = mongoose.model('User', userSchema)

module.exports = User;