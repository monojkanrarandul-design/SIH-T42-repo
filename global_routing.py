import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_3d_map():
    st.markdown("---")
    st.subheader("🌍 Tactical 3D Fleet Command Map")
    st.caption("Live global vessel distribution and chokepoint congestion.")

    # Synthetic coordinates mapping major global chokepoints
    data = {
        'lat': [30.5, 29.8, 31.2, 32.0, 1.3, 2.0, 1.5, 3.1, 0.8, 15.0, 16.5, 12.0, 18.0, 51.0, 52.0, -34.8, -35.2],
        'lon': [32.3, 32.5, 31.5, 33.1, 103.8, 102.5, 104.1, 101.2, 105.0, 115.0, 118.0, 112.0, 116.0, 2.5, 3.5, 20.0, 21.0],
        'vessel_type': ['Panamax', 'Capesize', 'Panamax', 'VLCC', 'VLCC', 'Panamax', 'Capesize', 'Panamax', 'Capesize', 'VLCC', 'Panamax', 'Capesize', 'Panamax', 'Capesize', 'VLCC', 'Panamax', 'Capesize'],
        'status': ['Congested', 'Congested', 'Routing', 'Moored', 'Routing', 'Congested', 'Routing', 'Routing', 'Moored', 'Routing', 'Routing', 'Moored', 'Routing', 'Moored', 'Routing', 'Routing', 'Routing'],
        'region': ['Suez', 'Suez', 'Suez', 'Suez', 'Malacca', 'Malacca', 'Malacca', 'Malacca', 'Malacca', 'South China Sea', 'South China Sea', 'South China Sea', 'South China Sea', 'North Sea', 'North Sea', 'Cape of Good Hope', 'Cape of Good Hope']
    }
    df = pd.DataFrame(data)

    # Color-code vessels by class (Neon UI theme)
    color_map = {'Panamax': '#00D2FF', 'Capesize': '#39FF14', 'VLCC': '#FFA500'}
    df['color'] = df['vessel_type'].map(color_map)

    fig = go.Figure()

    # Inject the vessel data onto the globe
    fig.add_trace(go.Scattergeo(
        lon=df['lon'],
        lat=df['lat'],
        text=df['vessel_type'] + ' | ' + df['status'] + ' | ' + df['region'],
        hoverinfo='text',
        mode='markers',
        marker=dict(
            size=9,
            color=df['color'],
            line=dict(width=1, color='white'),
            opacity=0.85
        )
    ))

    # Transform a flat map into an interactive 3D Globe
    fig.update_geos(
        projection_type="orthographic", # This specific parameter creates the 3D sphere
        showcoastlines=True,
        coastlinecolor="#2A2A2A",
        showland=True,
        landcolor="#161B22",
        showocean=True,
        oceancolor="#090C10",
        showlakes=False,
        showcountries=True,
        countrycolor="#1A1A1A",
        center=dict(lon=70, lat=15), # Centers the camera perfectly over the Indian Ocean
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        paper_bgcolor="rgba(0,0,0,0)", # Transparent background to blend into Streamlit
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)