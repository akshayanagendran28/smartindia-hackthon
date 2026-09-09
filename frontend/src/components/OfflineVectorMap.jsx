import React, { useState, useRef, useMemo } from 'react';
import { 
  Plus, Minus, RotateCcw, Compass, MapPin, Building2, 
  Landmark, ShieldCheck, Navigation, Sparkles, Eye, Info
} from 'lucide-react';

// India State Bounding Boxes & Viewport Presets
const STATE_VIEWPORTS = {
  all: { centerLat: 21.5, centerLon: 82.0, zoom: 1.0, name: 'National Overview (All India)' },
  'Tamil Nadu': { centerLat: 11.8, centerLon: 78.8, zoom: 3.2, name: 'Tamil Nadu (Tiruvallur / Chennai / Salem)' },
  'Maharashtra': { centerLat: 19.3, centerLon: 75.5, zoom: 2.8, name: 'Maharashtra (Mumbai / Pune / Nagpur)' },
  'Karnataka': { centerLat: 14.5, centerLon: 76.5, zoom: 2.9, name: 'Karnataka (Bengaluru / Mysuru)' },
  'Delhi': { centerLat: 28.6, centerLon: 77.2, zoom: 5.5, name: 'National Capital Region (Delhi)' },
  'Gujarat': { centerLat: 22.5, centerLon: 71.5, zoom: 2.8, name: 'Gujarat (Ahmedabad / Surat)' }
};

export default function OfflineVectorMap({ 
  branches = [], 
  selectedBranch = null, 
  onSelectBranch = () => {},
  selectedState = 'all'
}) {
  const [zoom, setZoom] = useState(1.0);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [hoveredBranch, setHoveredBranch] = useState(null);
  const containerRef = useRef(null);

  // Sync state preset viewport when state filter changes
  const activeViewport = useMemo(() => {
    return STATE_VIEWPORTS[selectedState] || STATE_VIEWPORTS.all;
  }, [selectedState]);

  // Dimensions of SVG Coordinate Space
  const SVG_WIDTH = 800;
  const SVG_HEIGHT = 700;

  // Equirectangular projection tailored for India's exact geographic bounds
  // Longitude range: 68.0° E to 97.5° E
  // Latitude range: 8.0° N to 37.0° N
  const project = (lat, lon) => {
    const minLon = 68.0;
    const maxLon = 97.5;
    const minLat = 7.5;
    const maxLat = 37.5;

    const x = ((lon - minLon) / (maxLon - minLon)) * SVG_WIDTH;
    const y = SVG_HEIGHT - ((lat - minLat) / (maxLat - minLat)) * SVG_HEIGHT;
    return { x, y };
  };

  // Center coordinate of the active view
  const viewCenter = useMemo(() => {
    return project(activeViewport.centerLat, activeViewport.centerLon);
  }, [activeViewport]);

  // Zoom controls
  const handleZoomIn = () => setZoom(prev => Math.min(prev * 1.3, 6.0));
  const handleZoomOut = () => setZoom(prev => Math.max(prev / 1.3, 0.8));
  const handleReset = () => {
    setZoom(activeViewport.zoom);
    setPan({ x: 0, y: 0 });
  };

  // Pan handlers
  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPan({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  const handleMouseUp = () => setIsDragging(false);

  // Transform matrix string for zoom & pan
  const currentZoom = zoom * (activeViewport.zoom || 1.0);
  const transformMatrix = `translate(${SVG_WIDTH / 2 + pan.x}, ${SVG_HEIGHT / 2 + pan.y}) scale(${currentZoom}) translate(${-viewCenter.x}, ${-viewCenter.y})`;

  return (
    <div 
      ref={containerRef}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      className="relative w-full h-full bg-slate-950 rounded-2xl overflow-hidden cursor-grab active:cursor-grabbing select-none"
      style={{ minHeight: '520px' }}
    >
      {/* Background Geo Grid Pattern */}
      <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:24px_24px] pointer-events-none" />

      {/* Top HUD Bar */}
      <div className="absolute top-3 left-3 right-3 z-20 flex items-center justify-between pointer-events-none">
        <div className="bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-700/80 shadow-lg flex items-center gap-2 pointer-events-auto">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block" />
          <span className="text-xs font-black text-white">Offline National Banking Map</span>
          <span className="text-[10px] bg-emerald-500/20 text-emerald-300 font-bold px-2 py-0.5 rounded-full border border-emerald-500/40">
            Razorpay IFSC
          </span>
        </div>

        {/* Viewport Indicator */}
        <div className="hidden sm:flex bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-700/80 shadow-lg text-[11px] text-slate-300 pointer-events-auto">
          <span className="font-bold text-emerald-400 mr-1.5">Region:</span>
          <span>{activeViewport.name}</span>
        </div>
      </div>

      {/* Interactive SVG Canvas */}
      <svg 
        viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`} 
        className="w-full h-full"
        style={{ touchAction: 'none' }}
      >
        <g transform={transformMatrix} className="transition-transform duration-300 ease-out">
          
          {/* India Boundary Polygons (Accurate Geographic Base Map) */}
          <g id="india-states-base">
            
            {/* North & Northwest Region (Jammu, Kashmir, Ladakh, Punjab, Haryana, Rajasthan, Delhi) */}
            <path
              d="M 230 40 L 265 20 L 320 25 L 340 70 L 325 110 L 360 140 L 305 180 L 280 160 L 250 170 L 230 140 L 205 150 L 195 210 L 130 250 L 110 320 L 220 330 L 260 270 L 280 280 L 270 230 L 300 220 L 310 190 Z"
              fill="#1e293b"
              stroke="#334155"
              strokeWidth={1.2 / currentZoom}
              className="hover:fill-slate-800 transition-colors"
            />
            
            {/* Central & Western Region (Gujarat, Maharashtra, Madhya Pradesh, Goa) */}
            <path
              d="M 110 320 L 70 340 L 60 375 L 120 400 L 100 440 L 160 430 L 170 470 L 190 530 L 220 540 L 240 500 L 280 470 L 340 450 L 390 410 L 380 340 L 330 300 L 260 270 L 220 330 Z"
              fill="#1e293b"
              stroke="#334155"
              strokeWidth={1.2 / currentZoom}
              className="hover:fill-slate-800 transition-colors"
            />

            {/* Southern Peninsula Region (Karnataka, Andhra Pradesh, Telangana, Tamil Nadu, Kerala) */}
            <path
              d="M 190 530 L 210 590 L 240 640 L 270 680 L 290 650 L 320 590 L 350 510 L 370 460 L 340 450 L 280 470 L 240 500 L 220 540 Z"
              fill="#1e293b"
              stroke="#334155"
              strokeWidth={1.2 / currentZoom}
              className="hover:fill-slate-800 transition-colors"
            />

            {/* Eastern & Central-Eastern Region (Uttar Pradesh, Bihar, Odisha, Jharkhand, West Bengal) */}
            <path
              d="M 300 220 L 360 210 L 440 240 L 510 260 L 530 320 L 500 370 L 460 410 L 390 410 L 340 450 L 380 340 L 330 300 L 270 230 Z"
              fill="#1e293b"
              stroke="#334155"
              strokeWidth={1.2 / currentZoom}
              className="hover:fill-slate-800 transition-colors"
            />

            {/* Northeast States Region (Assam, Meghalaya, Arunachal, Nagaland, Manipur, Mizoram, Tripura) */}
            <path
              d="M 530 260 L 590 220 L 670 220 L 690 260 L 650 300 L 660 350 L 620 380 L 580 340 L 540 330 Z"
              fill="#1e293b"
              stroke="#334155"
              strokeWidth={1.2 / currentZoom}
              className="hover:fill-slate-800 transition-colors"
            />
          </g>

          {/* State Boundary Outlines Highlight for Focus State */}
          {selectedState === 'Tamil Nadu' && (
            <path
              d="M 230 580 L 260 630 L 285 675 L 300 640 L 320 580 L 280 570 Z"
              fill="#065f46"
              fillOpacity="0.35"
              stroke="#10b981"
              strokeWidth={2 / currentZoom}
            />
          )}
          {selectedState === 'Maharashtra' && (
            <path
              d="M 120 400 L 100 440 L 160 430 L 170 470 L 220 540 L 280 470 L 340 450 L 330 390 L 240 410 Z"
              fill="#065f46"
              fillOpacity="0.35"
              stroke="#10b981"
              strokeWidth={2 / currentZoom}
            />
          )}
          {selectedState === 'Karnataka' && (
            <path
              d="M 170 470 L 190 530 L 210 590 L 240 600 L 260 550 L 240 500 L 220 540 Z"
              fill="#065f46"
              fillOpacity="0.35"
              stroke="#10b981"
              strokeWidth={2 / currentZoom}
            />
          )}

          {/* Major District / City Centroid Labels */}
          <g id="city-labels" className="pointer-events-none">
            {[
              { name: 'New Delhi', lat: 28.6139, lon: 77.2090 },
              { name: 'Mumbai', lat: 18.9298, lon: 72.8333 },
              { name: 'Chennai', lat: 13.0827, lon: 80.2707 },
              { name: 'Tiruvallur', lat: 13.1432, lon: 79.9082 },
              { name: 'Bengaluru', lat: 12.9716, lon: 77.5946 },
              { name: 'Pune', lat: 18.5204, lon: 73.8567 },
              { name: 'Ahmedabad', lat: 23.0225, lon: 72.5714 },
              { name: 'Kolkata', lat: 22.5726, lon: 88.3639 },
              { name: 'Hyderabad', lat: 17.3850, lon: 78.4867 }
            ].map((city) => {
              const pt = project(city.lat, city.lon);
              return (
                <g key={city.name}>
                  <circle cx={pt.x} cy={pt.y} r={2.5 / currentZoom} fill="#64748b" opacity="0.8" />
                  <text 
                    x={pt.x + (4 / currentZoom)} 
                    y={pt.y + (3 / currentZoom)} 
                    fontSize={10 / currentZoom} 
                    fill="#94a3b8" 
                    fontWeight="bold"
                    fontFamily="system-ui"
                  >
                    {city.name}
                  </text>
                </g>
              );
            })}
          </g>

          {/* Bank Branch Markers & Scheme Nodal Pins */}
          <g id="branch-markers">
            {branches.map((b) => {
              const lat = b.latitude || 13.1432;
              const lon = b.longitude || 79.9082;
              const pt = project(lat, lon);
              const isSelected = selectedBranch?.ifsc === b.ifsc;
              const isHovered = hoveredBranch?.ifsc === b.ifsc;
              const isLead = Boolean(b.lead_bank_flag);
              const isDIC = (b.bank || '').includes('DISTRICT INDUSTRIES');
              const isCSC = (b.bank || '').includes('COMMON SERVICE');

              // Color scheme
              let markerColor = '#10b981'; // Emerald standard bank
              let ringColor = '#34d399';
              if (isLead) {
                markerColor = '#f59e0b'; // Amber gold lead bank
                ringColor = '#fbbf24';
              } else if (isDIC) {
                markerColor = '#06b6d4'; // Cyan DIC
                ringColor = '#67e8f9';
              } else if (isCSC) {
                markerColor = '#a855f7'; // Purple CSC
                ringColor = '#c084fc';
              }

              const size = (isSelected ? 22 : (isHovered ? 18 : 14)) / currentZoom;

              return (
                <g 
                  key={b.ifsc}
                  transform={`translate(${pt.x}, ${pt.y})`}
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectBranch(b);
                  }}
                  onMouseEnter={() => setHoveredBranch(b)}
                  onMouseLeave={() => setHoveredBranch(null)}
                  className="cursor-pointer"
                >
                  {/* Selected Pulsing Aura */}
                  {isSelected && (
                    <circle
                      r={(size * 1.8)}
                      fill={markerColor}
                      fillOpacity="0.3"
                      className="animate-ping"
                    />
                  )}

                  {/* Outer Pin Drop Shadow */}
                  <circle
                    r={size / 2}
                    fill="#0f172a"
                    stroke={isSelected ? '#ffffff' : ringColor}
                    strokeWidth={(isSelected ? 3.0 : 1.8) / currentZoom}
                  />

                  {/* Inner Core Icon Marker */}
                  <circle
                    r={size / 3.2}
                    fill={markerColor}
                  />

                  {/* Star badge on Lead Banks */}
                  {isLead && (
                    <circle
                      cx={size / 3.5}
                      cy={-size / 3.5}
                      r={3.5 / currentZoom}
                      fill="#ffffff"
                      stroke="#f59e0b"
                      strokeWidth={1 / currentZoom}
                    />
                  )}

                  {/* Hover Tag Tooltip */}
                  {(isHovered || isSelected) && (
                    <g transform={`translate(0, ${-size * 0.9})`} className="pointer-events-none">
                      <rect
                        x={-65 / currentZoom}
                        y={-24 / currentZoom}
                        width={130 / currentZoom}
                        height={20 / currentZoom}
                        rx={5 / currentZoom}
                        fill="#0f172a"
                        fillOpacity="0.95"
                        stroke={markerColor}
                        strokeWidth={1 / currentZoom}
                      />
                      <text
                        x={0}
                        y={-10 / currentZoom}
                        textAnchor="middle"
                        fill="#ffffff"
                        fontSize={9 / currentZoom}
                        fontWeight="bold"
                        fontFamily="monospace"
                      >
                        {b.ifsc} • {b.branch.substring(0, 14)}
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </g>
        </g>
      </svg>

      {/* Floating Zoom & Map Controls (Top Right) */}
      <div className="absolute top-3 right-3 z-20 flex flex-col gap-1.5 bg-slate-900/90 backdrop-blur-md p-1.5 rounded-xl border border-slate-700/80 shadow-xl">
        <button
          onClick={handleZoomIn}
          title="Zoom In"
          className="p-2 hover:bg-slate-800 text-slate-200 hover:text-white rounded-lg transition-colors"
        >
          <Plus className="w-4 h-4" />
        </button>
        <button
          onClick={handleZoomOut}
          title="Zoom Out"
          className="p-2 hover:bg-slate-800 text-slate-200 hover:text-white rounded-lg transition-colors"
        >
          <Minus className="w-4 h-4" />
        </button>
        <button
          onClick={handleReset}
          title="Reset View"
          className="p-2 hover:bg-slate-800 text-emerald-400 hover:text-emerald-300 rounded-lg transition-colors border-t border-slate-700"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Bottom Telemetry Bar */}
      <div className="absolute bottom-3 left-3 right-3 z-20 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        
        {/* Coordinates readout */}
        <div className="bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-700/80 shadow-lg text-[11px] font-mono text-slate-400 pointer-events-auto flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-emerald-400">
            <Compass className="w-3.5 h-3.5" />
            <span>{selectedBranch?.latitude ? `${selectedBranch.latitude.toFixed(4)}° N, ${selectedBranch.longitude.toFixed(4)}° E` : '13.1432° N, 79.9082° E'}</span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="text-slate-300 font-bold">{branches.length} Banking Nodes Active</span>
        </div>

        {/* Legend */}
        <div className="bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-700/80 shadow-lg text-[10px] text-slate-300 pointer-events-auto flex items-center gap-3 font-medium">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 inline-block ring-1 ring-amber-300" />
            <span>Lead District Bank</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block ring-1 ring-emerald-400" />
            <span>Bank Branch</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 inline-block ring-1 ring-cyan-300" />
            <span>DIC Centre</span>
          </span>
        </div>
      </div>
    </div>
  );
}
