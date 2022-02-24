export class CourseAndYear {
  faculty: string;
  courses: Course[];
}
export class Course {
  coursename: string;
  urls: Url[];
}
export class Url {
  year: number;
  url: string;
}
