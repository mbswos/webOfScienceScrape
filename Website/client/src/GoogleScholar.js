import React, {useState, useEffect} from 'react';
import './App.css';
import '../node_modules/react-vis/dist/style.css';
import {FlexibleWidthXYPlot, 
  HorizontalBarSeries, 
  VerticalGridLines, 
  HorizontalGridLines, 
  XAxis, 
  YAxis,
  Treemap
} from 'react-vis';
import PublicationTable from './components/PublicationTable';

function useFetch(url){
  const defaultData = []
  const [data, updateData] = useState(defaultData)

  useEffect(() => {
    async function fetchData(){
      const response = await fetch(url)
      const json = await response.json()
      
      updateData(json)
    }
    fetchData()
  }, [url])
  return data
}

function useFetchGoogleScholar(){
  const url = 'http://localhost:3001/departments/googlescholar.json'
  return useFetch(url)
}

function getGSDepartmentData(gsRaw){
  var gsDepartmentsSumCitations = {};
  var gsDepartments = [];
  for(var i = 0; i < gsRaw.length; i++){
    var dep = gsRaw[i].DEPARTMENT_NAME;
    var authScoreString = gsRaw[i].CITEDBY
    if(authScoreString !== undefined && authScoreString !== null && authScoreString !== 'N/A'){
      var authorScore = parseFloat(authScoreString)
      if(!(dep in gsDepartmentsSumCitations) ) {
        gsDepartmentsSumCitations[dep] = {sum: authorScore, count: 1}
      } else if (dep in gsDepartmentsSumCitations){
        gsDepartmentsSumCitations[dep].sum += authorScore;
        gsDepartmentsSumCitations[dep].count++;
      }
    }
  }
  for(const [department, stats] of Object.entries(gsDepartmentsSumCitations)){
    gsDepartments.push({x:stats.sum, y:department});
  }

  return gsDepartments;
}

function getAuthorCitationData(gsRaw, score_name){
  var authors = [];
  
  for(var i = 0; i < gsRaw.length; i++){
    var name = gsRaw[i].LAST_NAME + ', ' + gsRaw[i].FIRST_NAME
    var authorScore = 0.0
    var authScoreString = gsRaw[i][score_name]

    if(authScoreString !== undefined && authScoreString !== null && authScoreString !== 'N/A'){
      authorScore = parseFloat(authScoreString)
    }

    var auth = {x:authorScore, y:name};
    authors.push(auth);
  }

  return authors;
}

function GoogleScholar(){
  var gsRaw = useFetchGoogleScholar()
  // need this to allow for page load
  var defaultGSData = [{
    'DEPARTMENT_ID': 1, 
    'DEPARTMENT_NAME': 'a', 
    'FIRST_NAME': 'b',
    'TFNAME':'b',
    'LAST_NAME': 'c',
    'comments':[{'comment':'comment'}]
  }]

  var defaultGS = [{x: 'a', y:1}, {x: 'b', y:2}]

  // handle page load
  if (gsRaw.length < 1){
    var gsDepartments = defaultGS
    var authorCitationScores = []
  } else{
    var gsDepartments = getGSDepartmentData(gsRaw)
    var authorCitationScores = getAuthorCitationData(gsRaw, 'CITEDBY')
    var authorHIndexScores = getAuthorCitationData(gsRaw, 'HINDEX')
    var authorI10IndexScores = getAuthorCitationData(gsRaw, 'I10INDEX')
  }

  // Note used publication table to display professor comments (technical debt)
  return (
    <div className="container">
      <h1 className="center-text">Google Scholar</h1>
      <div className="row">
        <div className="col-md-12">
          <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-250} height={400} margin={{left:200}}>
            <VerticalGridLines />
            <HorizontalGridLines />
            <XAxis />
            <YAxis />
            <HorizontalBarSeries data={gsDepartments} />
          </FlexibleWidthXYPlot>
        </div>
      </div>
      <h2 className="center-text">Citations</h2>
      <div className="row">
        <div className="col-md-12">
          <div className="scroll-div">
            <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-260} height={authorCitationScores.length * 20} margin={{left:200}}>
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis />
              <YAxis />
              <HorizontalBarSeries data={authorCitationScores} />
            </FlexibleWidthXYPlot>
          </div>
        </div>
      </div>
      <h2 className="center-text">h-index</h2>
      <div className="row">
        <div className="col-md-12">
          <div className="scroll-div">
            <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-260} height={authorCitationScores.length * 20} margin={{left:200}}>
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis />
              <YAxis />
              <HorizontalBarSeries data={authorHIndexScores} />
            </FlexibleWidthXYPlot>
          </div>
        </div>
      </div>
      <h2 className="center-text">i10-index</h2>
      <div className="row">
        <div className="col-md-12">
          <div className="scroll-div">
            <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-260} height={authorCitationScores.length * 20} margin={{left:200}}>
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis />
              <YAxis />
              <HorizontalBarSeries data={authorI10IndexScores} />
            </FlexibleWidthXYPlot>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GoogleScholar;
