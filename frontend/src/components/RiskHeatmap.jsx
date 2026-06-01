import { useEffect, useRef } from 'react'
import { GridComponent, TooltipComponent, VisualMapComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { HeatmapChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([GridComponent, HeatmapChart, TooltipComponent, VisualMapComponent, CanvasRenderer])

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
  low: '#86c66f',
  medium: '#facc15',
  high: '#f59e0b',
  extreme: '#dc2626',
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

function RiskHeatmap() {
  const chartRef = useRef(null)

  useEffect(() => {
    if (!chartRef.current) {
      return undefined
    }

    echarts.getInstanceByDom(chartRef.current)?.dispose()
    const chart = echarts.init(chartRef.current)
    chart.setOption(option)

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chart.dispose()
    }
  }, [])

  return (
    <div className="risk-heatmap-layout">
      <div className="risk-heatmap-chart" ref={chartRef} />
    </div>
  )
}

export default RiskHeatmap
