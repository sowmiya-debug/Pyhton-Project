import React, { useState, useEffect } from "react";
import axios from "axios";

function HomePage() {
  const [employee, setEmployee] = useState(null); // full employee data
  const [basicDetails, setBasicDetails] = useState(null); // editable basics
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      setError("You are not logged in!");
      setLoading(false);
      return;
    }

    // Fetch current employee details
    axios
      .get("http://127.0.0.1:8000/api/employee/me/", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(( response) => {
        setEmployee(response.data);
        setBasicDetails({
          name:response.data.name,
          age:response.data.age,
          gender:response.data.gender,
          contact:response.data.contact
        });
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching employee:", err);
        setError("Failed to load employee details");
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setBasicDetails({ ...basicDetails, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    const token = localStorage.getItem("access");
    axios
      .put(
        "http://127.0.0.1:8000/api/employee/update-request/",
        basicDetails,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((response) => {
        setEmployee({ ...employee, ...basicDetails });
        setIsEditing(false);
        alert("Basic details updated successfully!");
      })
      .catch((err) => {
        console.error("Error updating details:", err);
        alert("Failed to update details");
      });
  };

  if (loading) {
    return <div className="text-center mt-10">Loading employee details...</div>;
  }

  if (error) {
    return <div className="text-center mt-10 text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Welcome, {basicDetails.name} 👋</h2>

      {/* Basic Details */}
      <div className="p-4 mb-4 border rounded shadow">
        <h3 className="text-lg font-semibold mb-2">Basic Details</h3>
        {isEditing ? (
          <div className="space-y-2">
            <input
              type="text"
              name="name"
              value={basicDetails.name}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
            <input
              type="number"
              name="age"
              value={basicDetails.age}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
            <input
              type="text"
              name="gender"
              value={basicDetails.gender}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
            <input
              type="text"
              name="contact"
              value={basicDetails.contact}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
            <button
              onClick={handleSave}
              className="bg-green-500 text-white px-4 py-2 rounded mt-2"
            >
              Save
            </button>
          </div>
        ) : (
          <div>
            <p><strong>Name:</strong> {basicDetails.name}</p>
            <p><strong>Age:</strong> {basicDetails.age}</p>
            <p><strong>Gender:</strong> {basicDetails.gender}</p>
            <p><strong>Contact:</strong> {basicDetails.contact}</p>
            <button
              onClick={() => setIsEditing(true)}
              className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
            >
              Edit
            </button>
          </div>
        )}
      </div>

      {/* Additional Details */}
      <div className="p-4 mb-4 border rounded shadow">
        <h3 className="text-lg font-semibold mb-2">Additional Details</h3>
        <p><strong>Address:</strong> {employee.address}</p>
        <p><strong>Emergency Contact:</strong> {employee.emergency_contact}</p>
      </div>

      {/* Occupational Details */}
      <div className="p-4 mb-4 border rounded shadow">
        <h3 className="text-lg font-semibold mb-2">Occupational Details</h3>
        <p><strong>Occupation:</strong> {employee.department}</p>
        <p><strong>Department:</strong> {employee.designation}</p>
      </div>

      {/* Salary Details */}
      <div className="p-4 mb-4 border rounded shadow">
        <h3 className="text-lg font-semibold mb-2">Salary Details</h3>
        <p><strong>Salary:</strong> ₹{employee.basic_salary_pay}</p>
        <p><strong>Bonus:</strong> ₹{employee.salary_allowance}</p>
      </div>
    </div>
  );
}

export default HomePage;
