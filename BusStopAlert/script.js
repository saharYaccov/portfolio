// Global variables
let map;
let userMarker;
let stationMarker;
let routeLine;
let userLocation = null;

// Initialize map
function initMap() {
    // Center map on Israel by default
    map = L.map('map').setView([31.7683, 35.2137], 8);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19
    }).addTo(map);
}

// Get user's current location
function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('הדפדפן לא תומך בשירות מיקום'));
            return;
        }

        showStatus('מאתר את המיקום שלך...', 'info');

        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                // Add or update user marker
                if (userMarker) {
                    userMarker.setLatLng([userLocation.lat, userLocation.lng]);
                } else {
                    userMarker = L.marker([userLocation.lat, userLocation.lng], {
                        icon: L.divIcon({
                            className: 'custom-marker',
                            html: '<div style="background: #3B82F6; width: 20px; height: 20px; border-radius: 50%; border: 4px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
                            iconSize: [28, 28],
                            iconAnchor: [14, 14]
                        }),
                        title: 'המיקום שלך'
                    }).addTo(map);
                }

                // Center map on user location
                map.setView([userLocation.lat, userLocation.lng], 14);

                showStatus('המיקום אותר בהצלחה!', 'success');
                resolve(userLocation);
            },
            (error) => {
                let errorMessage = 'לא ניתן לאתר את המיקום';
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'נדרשת הרשאה לגישה למיקום';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'מידע מיקום לא זמין';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'בקשת מיקום פגה';
                        break;
                }
                showStatus(errorMessage, 'error');
                reject(new Error(errorMessage));
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    });
}

// Calculate distance using Haversine formula
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c;
    
    return distance;
}

// Convert degrees to radians
function toRad(degrees) {
    return degrees * (Math.PI / 180);
}

// Format distance for display
function formatDistance(km) {
    if (km < 1) {
        return `${Math.round(km * 1000)} מטר`;
    }
    return `${km.toFixed(2)} ק"מ`;
}

// Calculate walking time (assuming 5 km/h average walking speed)
function calculateWalkingTime(km) {
    const hours = km / 5;
    const minutes = Math.round(hours * 60);
    
    if (minutes < 1) {
        return 'פחות מדקה';
    } else if (minutes === 1) {
        return 'כדקה';
    } else if (minutes < 60) {
        return `כ-${minutes} דקות הליכה`;
    } else {
        const hrs = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return `כ-${hrs} שעות ו-${mins} דקות הליכה`;
    }
}

// Show status message
function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('status-message');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type} show`;
    
    setTimeout(() => {
        statusEl.classList.remove('show');
    }, 3000);
}

// Draw route line between user and station
function drawRouteLine(userLat, userLng, stationLat, stationLng) {
    // Remove existing line if any
    if (routeLine) {
        map.removeLayer(routeLine);
    }

    // Draw new line
    routeLine = L.polyline(
        [[userLat, userLng], [stationLat, stationLng]],
        {
            color: '#FF6B35',
            weight: 4,
            opacity: 0.7,
            dashArray: '10, 10',
            lineJoin: 'round'
        }
    ).addTo(map);

    // Fit map to show both markers
    const bounds = L.latLngBounds(
        [userLat, userLng],
        [stationLat, stationLng]
    );
    map.fitBounds(bounds, { padding: [50, 50] });
}

// Calculate and display distance
async function calculateAndDisplay() {
    const latInput = document.getElementById('lat-input');
    const lngInput = document.getElementById('lng-input');
    const calculateBtn = document.getElementById('calculate-btn');
    
    const stationLat = parseFloat(latInput.value);
    const stationLng = parseFloat(lngInput.value);

    // Validate inputs
    if (isNaN(stationLat) || isNaN(stationLng)) {
        showStatus('יש להזין קואורדינטות תקינות', 'error');
        return;
    }

    if (stationLat < -90 || stationLat > 90 || stationLng < -180 || stationLng > 180) {
        showStatus('קואורדינטות לא חוקיות', 'error');
        return;
    }

    // Add loading state
    calculateBtn.classList.add('loading');
    calculateBtn.disabled = true;

    try {
        // Get user location if not already obtained
        if (!userLocation) {
            await getUserLocation();
        }

        // Add or update station marker
        if (stationMarker) {
            stationMarker.setLatLng([stationLat, stationLng]);
        } else {
            stationMarker = L.marker([stationLat, stationLng], {
                icon: L.divIcon({
                    className: 'custom-marker',
                    html: '<div style="background: #FF6B35; width: 20px; height: 20px; border-radius: 50%; border: 4px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
                    iconSize: [28, 28],
                    iconAnchor: [14, 14]
                }),
                title: 'תחנת אוטובוס'
            }).addTo(map);
        }

        // Calculate distance
        const distance = calculateDistance(
            userLocation.lat,
            userLocation.lng,
            stationLat,
            stationLng
        );

        // Draw route line
        drawRouteLine(userLocation.lat, userLocation.lng, stationLat, stationLng);

        // Display results
        const resultsSection = document.getElementById('results-section');
        const distanceValue = document.getElementById('distance-value');
        const walkingTime = document.getElementById('walking-time');
        const userLocationEl = document.getElementById('user-location');
        const stationLocationEl = document.getElementById('station-location');

        distanceValue.textContent = formatDistance(distance);
        walkingTime.textContent = calculateWalkingTime(distance);
        userLocationEl.textContent = `${userLocation.lat.toFixed(6)}, ${userLocation.lng.toFixed(6)}`;
        stationLocationEl.textContent = `${stationLat.toFixed(6)}, ${stationLng.toFixed(6)}`;

        resultsSection.style.display = 'block';
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        showStatus('החישוב הושלם בהצלחה!', 'success');

    } catch (error) {
        console.error('Error:', error);
        showStatus(error.message, 'error');
    } finally {
        calculateBtn.classList.remove('loading');
        calculateBtn.disabled = false;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize map
    initMap();

    // Try to get user location on load
    getUserLocation().catch(err => {
        console.log('Could not get initial location:', err.message);
    });

    // Calculate button click
    const calculateBtn = document.getElementById('calculate-btn');
    calculateBtn.addEventListener('click', calculateAndDisplay);

    // Enter key in inputs
    const inputs = document.querySelectorAll('.input-field');
    inputs.forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                calculateAndDisplay();
            }
        });
    });

    // Add example coordinates button behavior (optional)
    // You can add buttons to populate example coordinates for testing
});

// Helper function to add example location (Haifa central bus station)
function useHaifaExample() {
    document.getElementById('lat-input').value = '32.8154';
    document.getElementById('lng-input').value = '34.9946';
    showStatus('נטענו קואורדינטות לדוגמה - תחנה מרכזית חיפה', 'info');
}

// Export for potential use in console
window.useHaifaExample = useHaifaExample;
