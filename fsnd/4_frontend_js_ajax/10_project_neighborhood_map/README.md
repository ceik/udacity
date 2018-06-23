# FSND Project 4 - Neighborhood Map

Neighborhood App that implements a OpenStreetMaps app, a filter functionality, and retrieves links to Wikipedia articles for points of interest

## Dependencies

The project uses the following libraries:
- KnockoutJS
- LeafletJS
- JQuery
- Bootstrap

It also uses Mapbox for the Leaflet tile Layer (see details below) and the Wikipedia API.

## To Run

Everything besides the request to Mapbox should run out of the box.

To use Mapbox, one must create a Mapbox account and use the provided access token. The token needs to go into line 45 in neighborhood.js.