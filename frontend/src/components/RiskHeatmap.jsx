import { useEffect, useRef } from 'react'
import { GridComponent, TooltipComponent, VisualMapComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { HeatmapChart, ScatterChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { impactScale, levels, probabilityScale, scaleValue } from '../constants/riskScale.js'

echarts.use([
  GridComponent,
  HeatmapChart,
  ScatterChart,
  TooltipComponent,
  VisualMapComponent,
  CanvasRenderer,
])

const probabilities = ['Improvável', 'Rara', 'Possível', 'Provável', 'Praticamente\nCerta']
const impacts = ['1', '2', '3', '4', '5']

const cells = [
  [
    { value: 1, code: 'RB', level: 'low' },
    { value: 2, code: 'RB', level: 'low' },
    { value: 3, code: 'RB', level: 'low' },
    { value: 4, code: 'RB', level: 'low' },
    { value: 5, code: 'RM', level: 'medium' },
  ],
  [
    { value: 2, code: 'RB', level: 'low' },
    { value: 4, code: 'RB', level: 'low' },
    { value: 6, code: 'RM', level: 'medium' },
    { value: 8, code: 'RM', level: 'medium' },
    { value: 10, code: 'RM', level: 'medium' },
  ],
  [
    { value: 3, code: 'RB', level: 'low' },
    { value: 6, code: 'RM', level: 'medium' },
    { value: 9, code: 'RM', level: 'medium' },
    { value: 12, code: 'RA', level: 'high' },
    { value: 15, code: 'RA', level: 'high' },
  ],
  [
    { value: 4, code: 'RB', level: 'low' },
    { value: 8, code: 'RM', level: 'medium' },
    { value: 12, code: 'RA', level: 'high' },
    { value: 16, code: 'RA', level: 'high' },
    { value: 20, code: 'RE', level: 'extreme' },
  ],
  [
    { value: 5, code: 'RM', level: 'medium' },
    { value: 10, code: 'RM', level: 'medium' },
    { value: 15, code: 'RA', level: 'high' },
    { value: 20, code: 'RE', level: 'extreme' },
    { value: 25, code: 'RE', level: 'extreme' },
  ],
]

const colors = {
  low: levels.BAIXO.color,
  medium: levels.MODERADO.color,
  high: levels.ALTO.color,
  extreme: levels.EXTREMO.color,
}

const heatmapData = cells.flatMap((row, yIndex) =>
  row.map((cell, xIndex) => ({
    value: [xIndex, yIndex, cell.value],
    riskCode: cell.code,
    itemStyle: {
      color: colors[cell.level],
    },
  })),
)

// Converte um marcador (probabilidade/impacto em rótulo) para coordenadas da matriz.
function markerToPoint(marker) {
  const p = scaleValue(probabilityScale, marker.probability)
  const i = scaleValue(impactScale, marker.impact)
  if (!p || !i) {
    return null
  }
  return {
    value: [p - 1, i - 1],
    name: marker.label,
    symbol: marker.kind === 'residual' ? 'circle' : 'pin',
    symbolSize: marker.kind === 'residual' ? 18 : 28,
    itemStyle: {
      color: marker.kind === 'residual' ? '#ffffff' : '#0f172a',
      borderColor: '#0f172a',
      borderWidth: 2,
    },
  }
}

function buildMarkerSeries(markers) {
  const points = (markers || []).map(markerToPoint).filter(Boolean)
  if (points.length === 0) {
    return []
  }
  return [
    {
      type: 'scatter',
      data: points,
      label: {
        show: true,
        position: 'top',
        color: '#0f172a',
        fontSize: 11,
        fontWeight: 700,
        formatter: ({ name }) => name,
      },
      tooltip: { formatter: ({ name }) => name },
      z: 5,
    },
  ]
}

const option = {
  animation: false,
  tooltip: {
    formatter: ({ data }) => {
      const [x, y, score] = data.value
      return `${probabilities[x].replace('\n', ' ')} / Impacto ${impacts[y]}<br/>Valor: ${score}<br/>Classe: ${data.riskCode}`
    },
  },
  grid: {
    top: 6,
    right: 14,
    bottom: 48,
    left: 48,
  },
  visualMap: {
    show: false,
    min: 0,
    max: 25,
    dimension: 2,
  },
  xAxis: {
    type: 'category',
    data: probabilities,
    name: 'Probabilidade',
    nameLocation: 'middle',
    nameGap: 36,
    axisLabel: {
      color: '#475569',
      fontSize: 10,
      fontWeight: 600,
      interval: 0,
      lineHeight: 14,
    },
    axisLine: { lineStyle: { color: '#cbd5e1', width: 1 } },
    axisTick: { show: false },
    splitArea: { show: false },
    splitLine: { show: true, lineStyle: { color: '#ffffff', width: 2 } },
  },
  yAxis: {
    type: 'category',
    data: impacts,
    name: 'Impacto',
    nameLocation: 'middle',
    nameGap: 27,
    axisLabel: {
      color: '#475569',
      fontSize: 12,
      fontWeight: 600,
    },
    axisLine: { lineStyle: { color: '#cbd5e1', width: 1 } },
    axisTick: { show: false },
    splitArea: { show: false },
    splitLine: { show: true, lineStyle: { color: '#ffffff', width: 2 } },
  },
  series: [
    {
      type: 'heatmap',
      data: heatmapData,
      label: {
        show: true,
        color: '#0f172a',
        fontSize: 13,
        fontFamily: 'Source Sans 3, sans-serif',
        fontWeight: 700,
        lineHeight: 17,
        formatter: ({ data }) => `${data.value[2]}\n${data.riskCode}`,
      },
      itemStyle: {
        borderColor: '#ffffff',
        borderWidth: 2,
        borderRadius: 4,
      },
      emphasis: {
        itemStyle: {
          borderColor: '#0f172a',
          borderWidth: 2,
          shadowBlur: 0,
        },
      },
    },
  ],
}

function RiskHeatmap({ markers }) {
  const chartRef = useRef(null)
  const markersKey = JSON.stringify(markers || [])

  useEffect(() => {
    if (!chartRef.current) {
      return undefined
    }

    echarts.getInstanceByDom(chartRef.current)?.dispose()
    const chart = echarts.init(chartRef.current)
    chart.setOption({
      ...option,
      series: [...option.series, ...buildMarkerSeries(markers)],
    })

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chart.dispose()
    }
    // markersKey serializa os marcadores para re-renderizar quando mudam.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [markersKey])

  return (
    <div className="risk-heatmap-layout">
      <div className="risk-heatmap-chart" ref={chartRef} />
    </div>
  )
}

export default RiskHeatmap
