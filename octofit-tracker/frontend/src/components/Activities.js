
import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const endpoint = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Fetching activities from:', endpoint);
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Fetched activities:', results);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching activities:', err);
        setLoading(false);
      });
  }, [endpoint]);

  if (loading) return <div className="text-center my-5"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div></div>;

  return (
    <div className="card shadow mb-4">
      <div className="card-header bg-primary text-white">
        <h2 className="h4 mb-0">Activities</h2>
      </div>
      <div className="card-body">
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Type</th>
                <th scope="col">Date</th>
                <th scope="col">Details</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity, idx) => (
                <tr key={activity.id || idx}>
                  <th scope="row">{activity.id || idx + 1}</th>
                  <td>{activity.name || '-'}</td>
                  <td>{activity.type || '-'}</td>
                  <td>{activity.date || '-'}</td>
                  <td>
                    <button className="btn btn-sm btn-outline-primary" type="button" disabled>
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Activities;
