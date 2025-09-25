import React, { useState, useEffect } from 'react';
import axios from 'axios';

// User Profile Form Component
const UserProfileForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    linkedin_url: '',
    github_url: '',
    university: '',
    email: '',
    bio: ''
  });
  
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const API_BASE_URL = 'http://127.0.0.1:8001';

  // Load profiles on component mount
  useEffect(() => {
    loadProfiles();
  }, []);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    try {
      // Filter out empty values
      const profileData = Object.entries(formData).reduce((acc, [key, value]) => {
        if (value.trim() !== '') {
          acc[key] = value.trim();
        }
        return acc;
      }, {});

      const response = await axios.post(`${API_BASE_URL}/api/profile`, profileData, {
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.data.success) {
        setMessage({
          text: `✅ Profile created successfully! Profile ID: ${response.data.profile_id}`,
          type: 'success'
        });
        
        // Reset form
        setFormData({
          name: '',
          linkedin_url: '',
          github_url: '',
          university: '',
          email: '',
          bio: ''
        });
        
        // Refresh profiles list
        loadProfiles();
      } else {
        setMessage({
          text: `❌ Error: ${response.data.error || 'Unknown error'}`,
          type: 'error'
        });
      }
    } catch (error) {
      setMessage({
        text: `❌ Network error: ${error.response?.data?.detail || error.message}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  // Load profiles from API
  const loadProfiles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/profiles`);
      
      if (response.data.success) {
        setProfiles(response.data.profiles);
      }
    } catch (error) {
      console.error('Error loading profiles:', error);
    }
  };

  // Delete profile
  const deleteProfile = async (profileId) => {
    if (!window.confirm('Are you sure you want to delete this profile?')) {
      return;
    }

    try {
      const response = await axios.delete(`${API_BASE_URL}/api/profile/${profileId}`);
      
      if (response.data.success) {
        setMessage({
          text: '✅ Profile deleted successfully',
          type: 'success'
        });
        loadProfiles(); // Refresh the list
      }
    } catch (error) {
      setMessage({
        text: `❌ Error deleting profile: ${error.response?.data?.detail || error.message}`,
        type: 'error'
      });
    }
  };

  return (
    <div className="user-profile-container">
      <style jsx>{`
        .user-profile-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: Arial, sans-serif;
        }
        
        .form-container {
          background-color: white;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          margin-bottom: 30px;
        }
        
        .form-title {
          color: #333;
          text-align: center;
          margin-bottom: 30px;
          font-size: 24px;
        }
        
        .form-group {
          margin-bottom: 20px;
        }
        
        .form-label {
          display: block;
          margin-bottom: 5px;
          font-weight: bold;
          color: #555;
        }
        
        .required {
          color: red;
        }
        
        .form-input,
        .form-textarea {
          width: 100%;
          padding: 12px;
          border: 2px solid #ddd;
          border-radius: 5px;
          font-size: 16px;
          box-sizing: border-box;
        }
        
        .form-input:focus,
        .form-textarea:focus {
          border-color: #007bff;
          outline: none;
        }
        
        .form-textarea {
          height: 100px;
          resize: vertical;
        }
        
        .submit-button {
          background-color: #007bff;
          color: white;
          padding: 12px 30px;
          border: none;
          border-radius: 5px;
          font-size: 16px;
          cursor: pointer;
          width: 100%;
        }
        
        .submit-button:hover {
          background-color: #0056b3;
        }
        
        .submit-button:disabled {
          background-color: #ccc;
          cursor: not-allowed;
        }
        
        .message {
          margin-top: 20px;
          padding: 10px;
          border-radius: 5px;
          text-align: center;
        }
        
        .message.success {
          background-color: #d4edda;
          color: #155724;
          border: 1px solid #c3e6cb;
        }
        
        .message.error {
          background-color: #f8d7da;
          color: #721c24;
          border: 1px solid #f5c6cb;
        }
        
        .profiles-section {
          background-color: white;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .profiles-title {
          color: #333;
          margin-bottom: 20px;
          font-size: 20px;
        }
        
        .profile-item {
          background-color: #f8f9fa;
          padding: 15px;
          margin-bottom: 10px;
          border-radius: 5px;
          border-left: 4px solid #007bff;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .profile-info {
          flex-grow: 1;
        }
        
        .profile-name {
          font-weight: bold;
          color: #333;
          margin-bottom: 5px;
        }
        
        .profile-details {
          font-size: 14px;
          color: #666;
        }
        
        .profile-links {
          font-size: 12px;
          color: #007bff;
          margin-top: 3px;
        }
        
        .profile-link {
          color: #007bff;
          text-decoration: none;
          margin-right: 10px;
        }
        
        .profile-link:hover {
          text-decoration: underline;
        }
        
        .delete-button {
          background-color: #dc3545;
          color: white;
          border: none;
          padding: 5px 10px;
          border-radius: 3px;
          cursor: pointer;
          font-size: 12px;
        }
        
        .delete-button:hover {
          background-color: #c82333;
        }
        
        .refresh-button {
          background-color: #28a745;
          color: white;
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          margin-bottom: 15px;
        }
        
        .refresh-button:hover {
          background-color: #218838;
        }
      `}</style>

      {/* Form Section */}
      <div className="form-container">
        <h1 className="form-title">📝 User Profile Submission</h1>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">
              Full Name <span className="required">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              className="form-input"
              value={formData.name}
              onChange={handleInputChange}
              required
              placeholder="Enter your full name"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="linkedin_url">LinkedIn URL</label>
            <input
              type="url"
              id="linkedin_url"
              name="linkedin_url"
              className="form-input"
              value={formData.linkedin_url}
              onChange={handleInputChange}
              placeholder="https://linkedin.com/in/yourprofile"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="github_url">GitHub URL</label>
            <input
              type="url"
              id="github_url"
              name="github_url"
              className="form-input"
              value={formData.github_url}
              onChange={handleInputChange}
              placeholder="https://github.com/yourusername"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="university">Affiliated University</label>
            <input
              type="text"
              id="university"
              name="university"
              className="form-input"
              value={formData.university}
              onChange={handleInputChange}
              placeholder="Enter your university name"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="your.email@example.com"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="bio">Bio/Description</label>
            <textarea
              id="bio"
              name="bio"
              className="form-textarea"
              value={formData.bio}
              onChange={handleInputChange}
              placeholder="Brief description about yourself (optional)"
            />
          </div>

          <button 
            type="submit" 
            className="submit-button" 
            disabled={loading}
          >
            {loading ? 'Submitting...' : 'Submit Profile'}
          </button>
        </form>

        {message.text && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}
      </div>

      {/* Profiles List Section */}
      <div className="profiles-section">
        <h2 className="profiles-title">📋 Existing Profiles</h2>
        
        <button 
          className="refresh-button" 
          onClick={loadProfiles}
        >
          Refresh Profiles
        </button>

        {profiles.length === 0 ? (
          <p>No profiles found.</p>
        ) : (
          profiles.map((profile) => (
            <div key={profile.profile_id} className="profile-item">
              <div className="profile-info">
                <div className="profile-name">{profile.name}</div>
                <div className="profile-details">
                  University: {profile.university || 'Not specified'} | 
                  Created: {new Date(profile.created_at).toLocaleDateString()} |
                  ID: {profile.profile_id}
                </div>
              </div>
              <button 
                className="delete-button"
                onClick={() => deleteProfile(profile.profile_id)}
              >
                Delete
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default UserProfileForm;