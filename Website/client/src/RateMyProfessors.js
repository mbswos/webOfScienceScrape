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

function useFetchRateMyProfessors(){
  const url = 'http://localhost:3001/departments/ratemyprofessors.json'
  return useFetch(url)
}

function getRMPDepartmentData(rmpRaw){
  var rmpDepartmentsAverage = {};
  var rmpDepartments = [];
  for(var i = 0; i < rmpRaw.length; i++){
    var dep = rmpRaw[i].DEPARTMENT_NAME;
    var authScoreString = rmpRaw[i].OVERALL_RATING
    if(authScoreString !== undefined && authScoreString !== null && authScoreString !== 'N/A'){
      var authorScore = parseFloat(authScoreString)
      if(!(dep in rmpDepartmentsAverage) ) {
        rmpDepartmentsAverage[dep] = {sum: authorScore, count: 1, average: authorScore}
      } else if (dep in rmpDepartmentsAverage){
        rmpDepartmentsAverage[dep].sum += authorScore;
        rmpDepartmentsAverage[dep].count++;
        rmpDepartmentsAverage[dep].average = rmpDepartmentsAverage[dep].sum/rmpDepartmentsAverage[dep].count;
      }
    }
  }
  for(const [department, stats] of Object.entries(rmpDepartmentsAverage)){
    rmpDepartments.push({x:stats.average, y:department});
  }

  return rmpDepartments;
}

function getAuthorAverageData(rmpRaw){
  var authors = [];
  for(var i = 0; i < rmpRaw.length; i++){
    var name = rmpRaw[i].LAST_NAME + ', ' + rmpRaw[i].FIRST_NAME
    var authorScore = 0.0
    var authScoreString = rmpRaw[i].OVERALL_RATING

    if(authScoreString !== undefined && authScoreString !== null && authScoreString !== 'N/A'){
      authorScore = parseFloat(authScoreString)
    }
    var auth = {x:authorScore, y:name};
    authors.push(auth);
  }

  return authors;
}

function getAuthorComments(rmpRaw){
  var authors = [];
  for(var i = 0; i < rmpRaw.length; i++){
    var author = {}
    author.LAST_NAME = rmpRaw[i].LAST_NAME
    author.FIRST_NAME = rmpRaw[i].FIRST_NAME
    author.publications = [];
    console.log(rmpRaw[i].ratingComments)
    if(rmpRaw[i].ratingComments !== undefined && rmpRaw[i].ratingComments !== null){
      for(var pub of rmpRaw[i].ratingComments){
        author.publications.push({title:pub.comment})
      }
      authors.push(author)
    }
  }
  console.log(authors)
  return authors
}

function RateMyProfessors(){
  var rmpRaw = useFetchRateMyProfessors()
  // need this to allow for page load
  var defaultRMPData = [{
    'DEPARTMENT_ID': 1, 
    'DEPARTMENT_NAME': 'a', 
    'FIRST_NAME': 'b',
    'TFNAME':'b',
    'LAST_NAME': 'c',
    'comments':[{'comment':'comment'}]
  }]

  var defaultRMP = [{x: 'a', y:1}, {x: 'b', y:2}]

  // handle page load
  if (rmpRaw.length < 1){
    var rmpDepartments = defaultRMP
    var authors = []
    var authorComments = [{'first_name': 'a', 'last_name': 'b', 'publications': [{'title':'a'}]}]
  } else{
    var rmpDepartments = getRMPDepartmentData(rmpRaw)
    var authors = getAuthorAverageData(rmpRaw)
    var authorComments = getAuthorComments(rmpRaw)
  }

  // Note used publication table to display professor comments (technical debt)
  return (
    <div className="container">
      <h1 className="center-text">RateMyProfessors</h1>
      <div className="row">
        <div className="col-md-12">
          <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-250} height={400} margin={{left:200}}>
            <VerticalGridLines />
            <HorizontalGridLines />
            <XAxis />
            <YAxis />
            <HorizontalBarSeries data={rmpDepartments} />
          </FlexibleWidthXYPlot>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <div className="scroll-div">
            <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-260} height={authors.length * 20} margin={{left:200}}>
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis />
              <YAxis />
              <HorizontalBarSeries data={authors} />
            </FlexibleWidthXYPlot>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <div className="scroll-div">
            <PublicationTable authorsAndPublications={authorComments}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RateMyProfessors;
