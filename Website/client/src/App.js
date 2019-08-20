import React, {useState, useEffect} from 'react';
import './App.css';
import '../node_modules/react-vis/dist/style.css';
import Publications from './Publications';
import RateMyProfessors from './RateMyProfessors';
import GoogleScholar from './GoogleScholar';
import {Tabs, Tab} from 'react-bootstrap';

function App(){
  const [key, setKey] = useState('publications');

  return (
    <div className="App">
      <Tabs id="controlled-tab-example" activeKey={key} onSelect={k => setKey(k)}>
        <Tab eventKey="publications" title="Publications">
          <Publications />
        </Tab>
        <Tab eventKey="ratemyprofessors" title="RateMyProfessors">
          <RateMyProfessors />
        </Tab>
        <Tab eventKey="googlescholar" title="GoogleScholar">
          <GoogleScholar />
        </Tab>
      </Tabs>
    </div>
  );

}

export default App;
