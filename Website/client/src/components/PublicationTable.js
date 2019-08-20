import React, {useState, useEffect} from 'react';

function PublicationTable(authorsAndPublications){
  var aAndP = authorsAndPublications.authorsAndPublications
  var authorRows = aAndP.map((author) => 
    {
      if(author.publications === null){
        return (
          <tr>       
            <td>{author.LAST_NAME} {author.FIRST_NAME}</td>
            <td>None</td>
          </tr>
        )
      }else{
        return (
          <tr>
            <td>{author.LAST_NAME} {author.FIRST_NAME}</td>
            {author.publications.map((publication) => <tr><td>{publication.title}</td></tr>)}        
          </tr>
        )
      }
    }
  )
  return (
    <table className="table table-sm table-striped table-bordered">
      <thead></thead>
      <tbody>{authorRows}</tbody>
    </table>
  );
}

export default PublicationTable