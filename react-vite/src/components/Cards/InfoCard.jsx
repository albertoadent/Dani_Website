import { Link } from "react-router-dom";

export default function InfoCardMain({
  header,
  subHeader,
  text,
  imageUrl,
  linkTo,
}) {
  if (!(header || subHeader || text || imageUrl || linkTo)) {
    return <div className="h-0 w-0 m-0 p-0"></div>;
  }

  return (
    <div
      className={`bg-cover h-80 flex flex-col justify-center align-center items-center w-full p-4 bg-card border-b-4 border-accent gap-2`}
      style={{ backgroundImage: `url(${imageUrl})` }}
    >
      <h1 className="bg-[var(--secondary-foreground)] text-popover p-2 rounded text-xl">
        {header}
      </h1>
      <h2 className="text-primary" style={{ textShadow: "2px 2px 4px black" }}>
        {subHeader}
      </h2>
      <p className="bg-[var(--card-foreground)] p-2 rounded text-input text-sm">
        {text}
      </p>
      {!!linkTo && <Link to={linkTo}>Learn More</Link>}
    </div>
  );
}

export function InfoCardSecondary({
  header,
  subHeader,
  text,
  imageUrl,
  linkTo,
}) {
  if (!(header || subHeader || text || imageUrl || linkTo)) {
    return <div className="h-0 w-0 m-0 p-0"></div>;
  }
  return (
    <div
      className={`bg-cover h-48 w-48 flex flex-col justify-evenly align-evenly items-center w-full p-4 bg-[var(--popover-foreground)] border-b-4 border-ring gap-[1px] rounded-[100%]`}
      style={{ backgroundImage: `url(${imageUrl})` }}
    >
      {!!header && (
        <h1 className="bg-card text-popover p-2 text-md text-center font-bold">
          {header}
          {!!subHeader && (
            <h2 className="text-primary text-sm border p-1 border-primary font-thin">
              {subHeader}
            </h2>
          )}
        </h1>
      )}
      {!header && !!subHeader && (
        <h1 className="bg-card text-popover p-2 text-md text-center font-bold">
          {!!subHeader && (
            <h2 className="text-primary text-sm border p-1 border-primary font-thin">
              {subHeader}
            </h2>
          )}
        </h1>
      )}

      {!!text && <p className="bg-card p-2 text-popover text-xs">{text}</p>}
      {!!linkTo && (
        <Link className="bg-ring rounded" to={linkTo}>
          Click Here
        </Link>
      )}
    </div>
  );
}
