// Simple toast replacement
const toast = {
  success: (message) => {
    console.log('SUCCESS:', message);
    alert(`✅ ${message}`);
  },
  error: (message) => {
    console.log('ERROR:', message);
    alert(`❌ ${message}`);
  },
  info: (message) => {
    console.log('INFO:', message);
    alert(`ℹ️ ${message}`);
  }
};

export default toast; 