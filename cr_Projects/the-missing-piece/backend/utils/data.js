// Shared data utilities for reading/writing JSON files
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.resolve(__dirname, '..', 'data');

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

function readData(filename) {
  ensureDir();
  const filePath = path.join(DATA_DIR, filename);
  if (!fs.existsSync(filePath)) {
    return null;
  }
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    console.error(`Error reading ${filename}:`, e.message);
    return null;
  }
}

function writeData(filename, data) {
  ensureDir();
  const filePath = path.join(DATA_DIR, filename);
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (e) {
    console.error(`Error writing ${filename}:`, e.message);
    return false;
  }
}

// Get data: returns the stored data if it exists, otherwise writes and returns the default
function getData(filename, defaultData) {
  const data = readData(filename);
  if (data === null) {
    writeData(filename, defaultData);
    return defaultData;
  }
  return data;
}

// Sanitize user input
function sanitizeInput(str) {
  if (typeof str !== 'string') return '';
  return str
    .trim()
    .replace(/[<>]/g, '')
    .substring(0, 1000);
}

module.exports = { readData, writeData, getData, sanitizeInput, DATA_DIR };
