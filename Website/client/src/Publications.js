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

function useFetchDepartmentPublications(){
  const url = 'http://localhost:3001/departments/publications.json'
  return useFetch(url)
}

function useFetchDepartments(){
  const url = 'http://localhost:3001/departments/'
  return useFetch(url)
}

function getDepartmentGraphData(departments){
  var pubDepartments = []
  for(var i = 0; i < departments.length; i++){
    var name = departments[i].DEPARTMENT_NAME;
    var count = departments[i].publication_count;
    pubDepartments.push({x:count, y:name})
  }
  return pubDepartments;
}

function getAuthorPublicationGraphData(publications){
  var pubAllAuthors = {title: '', children:[]}
  var pubAuthorsUTDallas = {title: '', children:[]}
  var pubAuthorsFinancialTimes = {title: '', children:[]}
  var pubAuthorsOther = {title: '', children:[]}

  var publicationsUTDallas = []
  var publicationsFinancialTimes = []
  var publicationsOther = []

  for(var i = 0; i < publications.length; i++){
    var name = publications[i].LAST_NAME + ', ' + publications[i].FIRST_NAME
    if(publications[i].publications && publications[i].publications.length > 0){
      var count = publications[i].publications.length
      var countUTDallas = 0
      var countFinancialTimes = 0
      var countOther = 0

      var authorUTDallas = {LAST_NAME: publications[i].LAST_NAME, FIRST_NAME: publications[i].FIRST_NAME, publications:[]}
      var authorFinancialTimes = {LAST_NAME: publications[i].LAST_NAME, FIRST_NAME: publications[i].FIRST_NAME, publications:[]}
      var authorOther = {LAST_NAME: publications[i].LAST_NAME, FIRST_NAME: publications[i].FIRST_NAME, publications:[]}

      for(var pub of publications[i].publications){
        if(pub.utdallas > 0){
          countUTDallas++;
          authorUTDallas.publications.push(pub)
        }

        if(pub.ftt50 > 0){
          countFinancialTimes++;
          authorFinancialTimes.publications.push(pub)
        }

        if(pub.ftt50 === 0 && pub.utdallas === 0){
          countOther++;
          authorOther.publications.push(pub)
        }
      }

      pubAllAuthors.children.push({title:name + ': ' + count, size:count})
      if(countUTDallas > 0){
        pubAuthorsUTDallas.children.push({title:name + ': ' + countUTDallas, size:countUTDallas})
        publicationsUTDallas.push(authorUTDallas)
      }
      if(countFinancialTimes > 0){
        pubAuthorsFinancialTimes.children.push({title:name + ': ' + countFinancialTimes, size:countFinancialTimes})
        publicationsFinancialTimes.push(authorFinancialTimes)
      }
      if(countOther > 0){
        pubAuthorsOther.children.push({title:name + ': ' + countOther, size:countOther})
        publicationsOther.push(authorOther)
      }
    }
  }

  var pubAuthors = {
    pubAllAuthors: pubAllAuthors, 
    pubAuthorsUTDallas: pubAuthorsUTDallas,
    pubAuthorsFinancialTimes: pubAuthorsFinancialTimes, 
    pubAuthorsOther: pubAuthorsOther,
    publicationsUTDallas: publicationsUTDallas,
    publicationsFinancialTimes: publicationsFinancialTimes, 
    publicationsOther: publicationsOther
  }
  return pubAuthors;
}

function Publications(){
  var publications = useFetchDepartmentPublications()
  var departments = useFetchDepartments()
  // need this to allow for page load
  var defaultBarGraph = [{'x': 1, 'y': 'a'}, {'x': 2, 'y': 'b'}]
  var defaultPublications = [{'first_name': 'a', 'last_name': 'b', 'publications': [{'title':'a'}]}]
  // handle page load
  if (publications.length < 1 || departments.length < 1){
    var pubDepartments = defaultBarGraph
    var pubAuthors = {
      pubAllAuthors:{'title':'t',children:[{'title':'t2',size:20},{title:'t3',size:10}]},
      pubAuthorsUTDallas:{'title':'t',children:[{'title':'t2',size:20},{title:'t3',size:10}]},
      pubAuthorsFinancialTimes:{'title':'t',children:[{'title':'t2',size:20},{title:'t3',size:10}]},
      pubAuthorsOther:{'title':'t',children:[{'title':'t2',size:20},{title:'t3',size:10}]},
      publicationsUTDallas:[],
      publicationsFinancialTimes:[],
      publicationsOther:[]
    }
    publications = defaultPublications
  } else{
    var pubDepartments = getDepartmentGraphData(departments)
    var pubAuthors = getAuthorPublicationGraphData(publications)
    var pubAllAuthors = pubAuthors.pubAllAuthors
    var pubAuthorsUTDallas = pubAuthors.pubAuthorsUTDallas
    var pubAuthorsFinancialTimes = pubAuthors.pubAuthorsFinancialTimes
    var pubAuthorsOther = pubAuthors.pubAuthorsOther
    console.log(pubAuthors)
  }

  return (
    <div className="container">
      <div className="row"><h1 className="center-text">Publications</h1></div>
      <div className="row">
        <div className="col-md-12 nopadding">
          <FlexibleWidthXYPlot yType="ordinal" width={window.innerWidth-250} height={400} margin={{left:200}}>
            <VerticalGridLines />
            <HorizontalGridLines />
            <XAxis />
            <YAxis />
            <HorizontalBarSeries data={pubDepartments} />
          </FlexibleWidthXYPlot>
        </div>
      </div>
      <div className="row"><h2 className="center-text">All Publications</h2></div>
      <div className="row">
        <div className="col-md-6 col-sm-12 nopadding">
          <Treemap
            {...{
              width: window.innerWidth/2 - 61,
              height: 400,
              data: pubAllAuthors,
              mode: 'binary',
              style:{
                border: 'thin solid #ddd'
              }
            }}
          />
        </div>
        <div className="col-md-6 col-sm-12 nopadding">
          <div className="scroll-div">
            <PublicationTable authorsAndPublications={publications}/>
          </div>
        </div>  
      </div>
      <div className="row"><h2 className="center-text">UTDallas Publications</h2></div>
      <div className="row">
        <div className="col-md-6 col-sm-12 nopadding">
          <Treemap
            {...{
              width: window.innerWidth/2 - 61,
              height: 400,
              data: pubAuthorsUTDallas,
              mode: 'binary',
              style:{
                border: 'thin solid #ddd'
              }
            }}
          />
        </div>
        <div className="col-md-6 col-sm-12 nopadding">
          <div className="scroll-div">
            <PublicationTable authorsAndPublications={pubAuthors.publicationsUTDallas}/>
          </div>
        </div>
      </div>
      <div className="row"><h2 className="center-text">FinancialTimes Publications</h2></div>
      <div className="row">
        <div className="col-md-6 col-sm-12 nopadding">
          <Treemap
            {...{
              width: window.innerWidth/2 - 61,
              height: 400,
              data: pubAuthorsFinancialTimes,
              mode: 'binary',
              style:{
                border: 'thin solid #ddd'
              }
            }}
          />
        </div>
        <div className="col-md-6 col-sm-12 nopadding">
          <div className="scroll-div">
            <PublicationTable authorsAndPublications={pubAuthors.publicationsFinancialTimes}/>
          </div>
        </div>
      </div>
      <div className="row"><h2 className="center-text">Other Publications</h2></div>
      <div className="row">
        <div className="col-md-6 col-sm-12 nopadding">
          <Treemap
            {...{
              width: window.innerWidth/2 - 61,
              height: 400,
              data: pubAuthorsOther,
              mode: 'binary',
              style:{
                border: 'thin solid #ddd'
              }
            }}
          />
        </div>
        <div className="col-md-6 col-sm-12 nopadding">
          <div className="scroll-div">
            <PublicationTable authorsAndPublications={pubAuthors.publicationsOther}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Publications;
