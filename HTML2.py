<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Hello - get CGI Program</title>
    </head>

    <body>
        <form action="/cgi-bin/hello_get2.py" method="post">
            <label class="form-label">First Name: </label>
            <input class="form-control" type="text" name="first_name"> <br/>
            <label class="form-label">Last Name: </label>
            <input class="form-control" type="text" name="last_name" />
            <input class="btn btn-primary" type="submit" value="Submit" />
        </form>
    </body>
</html>

