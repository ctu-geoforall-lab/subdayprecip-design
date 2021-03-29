<template>
  <div class="rain-chart">
    <div class="table">
      <label>Číslo povodí:</label>
      <span v-text="attributes.id"/>
      <label>Výměra:</label>
      <span>{{ attributes.area }} km<sup>2</sup></span>
      <label>Úhrn návrhové srážky:</label>
      <span>{{ attributes.rainfall }} mm</span>
    </div>
    <div class="title">Průběh návrhových srážek</div>
    <plot-chart
      v-if="bandsData"
      height="200"
      :bands="bands"
      :data="bandsData"
      :x-axis="xAxis"
      :y-axis="yAxis"
    >
      <template v-slot:svg-layer>
        <path
          v-for="(curve, key) in curves"
          :key="`line-${key}`"
          :class="`line data-${key}`"
          :style="colorStyles[key]"
          :d="curve"
        />
      </template>
      <template v-slot:top-overlay>
        <div class="legend my-2">
          <div
            v-for="(band, key) in bands"
            :key="key"
            class="item"
          >
            <div class="dot" :style="colorStyles[key]"/>
            <span v-text="band.label"/>
          </div>
        </div>

        <div
          class="interactive"
          @mousemove="onMouseMove"
          @mouseover="tooltipVisible = true"
          @mouseleave="tooltipVisible = false"
        >
          <div
            v-if="tooltipVisible && tooltip"
            class="tooltip"
            :class="tooltip.align"
            :style="tooltip.style"
          >
            <span class="time">{{ tooltip.time }} min.</span>
            <div class="values">
              <span
                v-for="(value, band) in tooltip.data"
                :key="band"
                :style="colorStyles[band]"
                v-text="value"
              />
            </div>
          </div>
        </div>
      </template>
    </plot-chart>
    <div class="subtitle">Pravděpodobnosti výskytu návrhových průběhů</div>
    <div class="bar-chart">
      <div
        v-for="(item, i) in barChart"
        :key="i"
        class="item"
        :style="item.style"
      >
        {{ item.value }}%
      </div>
    </div>

    <a class="download" @click="download">Data CSV</a>
  </div>
</template>

<script>
import * as d3 from './d3-min'
import groupBy from 'lodash/groupBy'
import invert from 'lodash/invert'
import mapValues from 'lodash/mapValues'
import pick from 'lodash/pick'
import throttle from 'lodash/throttle'
import { saveAs } from 'file-saver'

import PlotChart, { bandsExtent } from './PlotChart.vue'
// import data from './rain.json'

import { getFeatureQuery, layerFeaturesQuery } from '@/map/featureinfo'

export default {
  name: 'RainChart',
  components: { PlotChart },
  props: {
    layer: Object,
    feature: Object,
    // rainfallAttribute: {
    //   type: String,
    //   default: 'h_n2t360'
    // }
  },
  data () {
    return {
      features: null, //data.features,
      tooltip: null,
      tooltipVisible: false
    }
  },
  computed: {
    config () {
      return this.$store.state.project.config
    },
    hn () {
      // povodi_iv_2_lete_6h
      return this.layer.name.split('_')[2]
    },
    rainfallAttribute () {
      return `h_n${this.hn}t360`
    },
    properties () {
      return this.feature.getProperties()
    },
    attributes () {
      return {
        id: this.feature.get('chp'),
        area: this.feature.get('a_km2').toFixed(2),
        rainfall: this.feature.get(this.rainfallAttribute)?.toFixed(1)
      }
    },
    bands () {
      return {
        A: {
          label: 'Typ A',
          color: 'rgb(255,0,0)'
        },
        B: {
          label: 'Typ B',
          color: 'rgb(255,124,128)'
        },
        C: {
          label: 'Typ C',
          color: 'rgb(255,192,0)'
        },
        D: {
          label: 'Typ D',
          color: 'rgb(25,255,0)'
        },
        E: {
          label: 'Typ E',
          color: 'rgb(146,208,80)'
        },
        F: {
          label: 'Typ F',
          color: 'rgb(0,112,192)'
        }
      }
    },
    colorStyles () {
      return mapValues(this.bands, g => ({ '--color': g.color }))
    },
    bandsData () {
      if (this.features) {
        return mapValues(this.features, features => features.map(f => ({
          time: parseInt(f.properties['T_(min)']),
          value: (f.properties['H5min_(%)'] / 100.0) * this.feature.get(this.rainfallAttribute)
        })))
      }
      return null
    },
    xAxis () {
      const w = 100
      const scale = d3.scaleLinear().range([0, w])
      scale.domain([0, 360])

      return {
        scale,
        ticks: d3.range(0, 365, 60)
      }
    },
    yAxis () {
      const h = 100
      const scale = d3.scaleLinear().range([h, 0])

      const [min, max] = bandsExtent(this.bandsData, d => d.value)
      // const [min, max] = d3.extent(this.chartData, d => d.value)
      scale.domain([min, max]).nice(4)
      // scale.domain([0, 10])
      return {
        scale,
        ticks: scale.ticks(6)
      }
    },
    curves () {
      if (this.bandsData) {
        const bands = Object.keys(this.bands).reverse()
        const datasets = pick(this.bandsData, bands)
        return mapValues(datasets, dataset => {
          const line = d3.line()
            .curve(d3.curveCardinal)
            .x(d => this.xAxis.scale(d.time))
            .y(d => this.yAxis.scale(d.value))
          return line(dataset)
        })
      }
    },
    barChart () {
      const prefix = `p_n${this.hn}typ`
      return Object.keys(this.bands).map(type => {
        const attr = prefix + type.toLowerCase()
        const value = this.feature.get(attr)
        return {
          value,
          style: {
            width: value + '%',
            '--color': this.bands[type].color
          }
        }
      })
    }
  },
  async created () {
    const features = await this.fetchData()
    this.features = features
  },
  methods: {
    async fetchData () {
      const bandLayers = mapValues(this.bands, ((v, id) => `typ${id}`))
      const queries = Object.values(bandLayers).map(name => layerFeaturesQuery({ name }))
      const query = getFeatureQuery(queries)
      const params = {
        'VERSION': '1.1.0',
        'SERVICE': 'WFS',
        'REQUEST': 'GetFeature',
        'OUTPUTFORMAT': 'GeoJSON',
        'MAXFEATURES': 1000
      }
      const { data } = await this.$http.post(this.config.ows_url, query, { params, headers: { 'Content-Type': 'text/xml' } })
      const layersBands = invert(bandLayers)
      return groupBy(data.features, f => layersBands[f.id.split('.')[0]])
    },
    // onMouseMove (e) {
    onMouseMove: throttle(function (e) {
      const offsetX = e.layerX || e.offsetX
      const x = this.xAxis.scale.invert(100 * offsetX / e.target.clientWidth)
      const time = Math.round(x / 5) * 5
      if (this.tooltip?.time !== time) {
        this.tooltip = {
          style: {
            left: this.xAxis.scale(time) + '%'
          },
          align: time < 300 ? 'right' : 'left',
          time,
          data: mapValues(this.bandsData, dataset => dataset.find(d => d.time === time)?.value.toFixed(3))
        }
      }
    }, 50),
    download (e) {
      const types = Object.keys(this.bands)
      const header = [
        'CAS_min',
        ...types.map(t => `H_N${this.hn}typ${t}_mm`),
        ...types.map(t => `P_N${this.hn}typ${t}_%`)
      ]
      const csv = [header.join(',')]
      const firstLine = '0,,,,,,' + types.map(type => this.feature.get(`p_n${this.hn}typ${type.toLowerCase()}`)).join(',')
      csv.push(firstLine)
      
      const times = this.bandsData[types[0]].map(i => i.time)
      times.forEach((time, index) => {
        const data = [time, ...types.map(type => this.bandsData[type][index].value.toFixed(3))]
        csv.push(data.join(',') + ',,,,,,')
      })
      // const data = times.map((time, index) => {
      //   return [time, ...types.map(type => this.bandsData[type][index].value.toFixed(3))]
      // })
      // csv.push(...data.map(row => row.join(',') + ',,,,,,'))
      // console.log(csv)
      const blob = new Blob([csv.join('\n')], { type: 'text/plain;charset=utf-8' })
      saveAs(blob, `${this.attributes.id}_N${this.hn}.csv`)
    }
  }
}
</script>

<style lang="scss" scoped>
.rain-chart {
  display: flex;
  flex-direction: column;
  .table {
    padding: 8px;
    display: grid;
    grid-template-columns: auto auto;
    label {
      font-weight: bold;
    }
  }
  .title {
    font-size: 18px;
    margin: 12px 8px;
    font-weight: bold;
    text-align: center;
  }
  .subtitle {
    font-size: 16px;
    margin: 8px;
    font-weight: bold;
    text-align: center;
  }
  .chart {
    padding-top: 32px;
    .line {
      fill: none;
      // stroke: currentColor;
      stroke: var(--color);
      stroke-width: 2;
      vector-effect: non-scaling-stroke;
    }
    .legend {
      position: absolute;
      top: 0;
      right: 0;
      display: flex;
      flex-direction: column;
      font-size: 12px;
      background-color: #fff;
      .item {
        display: flex;
        align-items: center;
        margin: 0 6px;
        .dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background-color: var(--color);
          flex-shrink: 0;
          margin-right: 6px;
        }
      }
    }
    .interactive {
      position: absolute;
      width: 100%;
      height: 100%;
      .tooltip {
        position: absolute;
        height: 100%;
        border-left: 1px solid #999;
        pointer-events: none;
        font-size: 13px;
        .time {
          position: absolute;
          white-space: nowrap;
          transform: translate(0, -100%);
          font-weight: bold;
        }
        .values {
          display: flex;
          flex-direction: column;
          background-color: #fcfcfc;
          border-radius: 3px;
          // border: 1px solid #ddd;
          margin: 0 3px;
          padding: 0 4px;
          box-shadow:
            0 3px 4px 0 rgba(0,0,0,.14),
            0 1px 8px 0 rgba(0,0,0,.12);
          > * {
            color: var(--color);
          }
        }
        &.left {
          .time {
            transform: translate(-100%, -100%);
          }
          .values {
            transform: translate(calc(-100% - 6px), 0);
          }
        }
      }
    }
  }
  .bar-chart {
    display: flex;
    align-items: center;
    gap: 1px;
    background-color: #444;
    border: 1px solid #444;
    border-width: 0 1px;
    height: 20px;
    font-size: 12px;
    margin: 8px;
    .item {
      background-color: var(--color);
      text-align: center;
    }
  }
  .download {
    align-self: center;
    padding: 2px 8px;
  }
}
</style>
