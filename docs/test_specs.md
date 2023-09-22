## projects
Acceptance Tests
* GET all projects
* POST create project
* POST update project
* DELETE project
* GET project

Functional Tests
* POST create project, verify error when reach limit of projects (Negative)
* POST Update project deleted, verify error when a project has been deleted

## Tasks
Acceptance Test
* GET Get active tasks
* POST Create a new task
* GET Get an active task
* POST Update a task
* POST Close a task
* POST Reopen a task
* DELETE Delete a task

Functional Tests
* POST Try to create a task without send nothing => Verify bad request 400  and
message related to "content must be provided"
* POST Try to create a task with duration_unit => Verify bad request 400  and
message related to "Item duration is missing..." 
* POST Try to create a task with duration => Verify bad request 400  and
message related to "Item duration unit is missing" 


## Section
Acceptance Test
* Get all sections
* Create a new section
* Get a single section
* Update a section
* Delete a section

Functional Tests
* POST create section, verify error when request is sent without project id => error 
404 not found and message Project not found
* DELETE section, verify error when request is sent with invalid id section like "abe"
=> 400 bad request and "section_id is invalid" message  displayed


## Comments
Acceptance Test
* Get all comments
* Create a new comment
* Get a comment
* Update a comment
* Delete a comment

Functional Tests
* GET comments, verify error when get comments request does not have id (Negative)
=>error 400 and "No id to filter notes provided"
* GET comments, verify empty list is gotten when the id is invalid

## Labels
Acceptance Test
* Add a personal label
* Update a personal label
* Delete a personal label
* Rename a shared label
* Delete shared label occurrences
* Update multiple label orders

Functional Tests
* GET a personal label, verify error when request is sent with invalid id label like "sd" or 1
=> 400 bad request and "Label not found" message  displayed
*  POST create a personal label, Verify error when request is sent with invalid color like "nada" or 1
=> 400 bad request and "color format is not valid" message  displayed


E2E Test 
* Verify a project can be created with comments and sections, every section with at least two tasks, one task with label
* Verify comments and label continue in the task reopened.