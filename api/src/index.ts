import express, { NextFunction, Request, Response } from "express";
import { MongoClient } from "mongodb";
import createError, { HttpError } from "http-errors";
import { Course, Url } from "./types";

(async () => {
  const uri = process.env.MONGODB as string;
  const client = new MongoClient(uri);
  await client.connect();
  const database = client.db("ntubot");

  const app = express();
  app.use(express.json());
  const port = 3000;

  app.put(
    "/putuser",
    async (req: Request, res: Response, next: NextFunction) => {
      const { _id, username } = req.body;
      const collection = database.collection("studentinfo");
      // try block should only produce one error, if produce more than one error compiler wont know whats the type of err
      try {
        // always need to await when dealing with database
        await collection.insertOne({ _id: _id, username: username });
      } catch (err) {
        next(createError(409, "User already exists"));
        return;
      }
      res.status(201).json(true);
    }
  );
  app.get(
    "/getfaculty",
    async (_req: Request, res: Response, next: NextFunction) => {
      const collection = database.collection("courseandyear");
      let result: string[];
      try {
        const data = await collection.find({}).toArray();
        result = data.map((x) => x.faculty);
      } catch (err) {
        next(err);
        return;
      }
      res.status(200).json(result);
    }
  );
  app.get(
    "/getcourse/:faculty",
    async (req: Request, res: Response, next: NextFunction) => {
      const faculty = req.params.faculty;
      const collection = database.collection("courseandyear");
      let result: string[];
      try {
        const data = await collection.findOne({ faculty: faculty });
        if (!data) {
          next(createError(404, "Faculty not found"));
          return;
        }
        result = data.courses.map((x: Course) => x.coursename);
      } catch (err) {
        console.log(err);
        next(err);
        return;
      }
      res.status(200).json(result);
    }
  );
  // next(err) will call this function
  app.get(
    "/geturls/:coursename",
    async (req: Request, res: Response, next: NextFunction) => {
      const coursename = req.params.coursename;
      console.log(coursename);
      const collection = database.collection("courseandyear");
      let result: Url[] = [];
      try {
        const data = await collection.findOne({
          "courses.coursename": coursename,
        });
        if (!data) {
          next(createError(404, "Course not found"));
          return;
        }

        const courses = data.courses as Course[];
        for (let i = 0; i < courses.length; i++) {
          if (courses[i].coursename == coursename) result = courses[i].urls;
        }
      } catch (err) {
        console.log(err);
        next(err);
        return;
      }
      if (!result) {
        next(createError(404, "Urls not found"));
      }
      res.status(200).json(result);
    }
  );
  app.use(
    (err: any, _req: Request, res: Response, _next: NextFunction): void => {
      if (err instanceof HttpError) {
        res.status(err.status).json(err.message);
      } else {
        res.status(500).json("Something went wrong");
      }
    }
  );
  app.listen(port, () => {
    console.log(`Server started on port ${port}`);
  });
})();
