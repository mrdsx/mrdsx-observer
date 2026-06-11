const NOT_FOUND = "NOT_FOUND";

class NotFoundError extends Error {
  code = NOT_FOUND;

  constructor(message: string) {
    super(message);
    this.name = "NotFoundError";
  }
}

export { NOT_FOUND, NotFoundError };
