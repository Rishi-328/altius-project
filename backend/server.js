const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose')

const app = express();
const PORT = 5000;
const JWT_SECRET = 'your_jwt_secret_key'; // Change this to a strong secret in production

app.use(cors());
app.use(bodyParser.json());

// In-memory user store (replace with DB in production)
mongoose.connect('mongodb://localhost:27017/altiusinter', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

const schema = new mongoose.Schema({
  username: { type: String, required: true, unique: true }, 
    password: { type: String, required: true }
});
const User = mongoose.model('User', schema);

// Signup route
app.post('/signup', async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password)
    return res.status(400).json({ message: 'Username and password required' });

  const user = await User.findOne({username});
  if(user){
    return res.status(400).json({ message: 'Username already exists' });
  }
  const hashedPassword = await bcrypt.hash(password, 10);
  const newUser = new User({username,password:hashedPassword})
  await newUser.save();

  res.status(201).json({ message: 'User created successfully' });
});

// Login route
app.post('/login', async (req, res) => {
    console.log("came")
  const { username, password } = req.body;
  if (!username || !password)
    return res.status(400).json({ message: 'Username and password required' });

    const user = await User.findOne({ username });
  if (!user)
    return res.status(401).json({ message: 'Invalid credentials' });

  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch)
    return res.status(401).json({ message: 'Invalid credentials' });

  const token = jwt.sign({ username }, JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
});

// Protected route example
app.get('/profile', (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader)
    return res.status(401).json({ message: 'No token provided' });

  const token = authHeader.split(' ')[1];
  jwt.verify(token, JWT_SECRET, (err, decoded) => {
    if (err)
      return res.status(401).json({ message: 'Invalid token' });

    res.json({ message: `Welcome, ${decoded.username}` });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

