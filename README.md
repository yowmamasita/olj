# Skills Mind Map Visualization

An interactive mind map visualization for hierarchical skills data using D3.js.

## Features

- **Interactive Radial Tree Layout**: Skills are displayed in a circular, mind map-like visualization
- **Progressive Disclosure**: Click nodes to expand/collapse one level at a time
- **Visual Indicators**: Dashed borders indicate nodes with hidden children
- **Search Functionality**: Find specific skills quickly
- **Zoom and Pan**: Navigate large skill trees easily
- **Color Coding**: Skills are color-coded by top-level category

## Files

- `allskills.json` - Cleaned skills data (HTML tags removed, &raquo; replaced with »)
- `allskills_tree_clean.json` - Hierarchical tree structure with IDs at leaf nodes
- `allskills_tree.json` - Tree structure with IDs at every node
- `allskills_id_mapping.json` - Mapping of full skill paths to their IDs
- `skills_mindmap.html` - The main visualization page
- `start_server.sh` - Script to start a local web server

## Usage

1. Start the local web server:
   ```bash
   ./start_server.sh
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/skills_mindmap.html
   ```

## Controls

- **Click** on nodes to expand/collapse their children
- **Drag** to pan around the visualization
- **Scroll** to zoom in/out
- **Search** for specific skills using the search box
- **Reset View** to center the visualization
- **Expand All** to show all nodes
- **Collapse All** to show only top-level categories

## Data Structure

The skills data is organized hierarchically with the following structure:
- Top-level categories (e.g., "Accounting", "Marketing", "Design")
- Subcategories and specializations
- Specific skills and tools at the leaf nodes

Each skill has a unique ID that can be used for tracking or integration with other systems.

## Technical Details

- Built with D3.js v7
- Uses radial tree layout for mind map visualization
- Responsive design that adapts to window size
- Smooth transitions when expanding/collapsing nodes

## Browser Compatibility

Works best in modern browsers that support ES6 and SVG:
- Chrome/Edge (recommended)
- Firefox
- Safari

## License

This project is provided as-is for visualization of skills data.