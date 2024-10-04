import { Link } from "react-router-dom";

export default function WorkshopCard({
  header,
  subHeader,
  text,
  imageUrl,
  index,
  linkTo,
}) {
  let rest = `bg-cover rounded-lg lg:p-10 p-2 sm:p-2 h-full w-full justify-center items-center`;
  const className4 = `bg-[url(/vines.png)]  ${rest}`;
  let className = className4;

  if (imageUrl) {
    
  }

  if (linkTo) {
    return (
      <Link
        className={className}
        style={{
          WebkitBackgroundSize: "cover",
          MozBackgroundSize: "cover",
          OBackgroundSize: "cover",
        }}
        to={linkTo}
      >
        <div className="h-full w-full bg-muted border border-input rounded-lg flex flex-col content-center items-center justify-items-center justify-center">
          {header && (
            <h3 className="text-white text-base md:text-xs font-bold text-center">
              {header}
            </h3>
          )}
          {subHeader && (
            <h4 className="text-accent text-sm md:text-xs p-2">{subHeader}</h4>
          )}
          {text && (
            <p className="bg-white rounded m-2 text-foreground p-2 text-xs md:text-xs">
              {text}
            </p>
          )}
          <h1 className="text-popover text-center bg-[var(--muted-foreground)] rounded p-1">
            SCHEDULE YOUR WORKSHOP
          </h1>
        </div>
      </Link>
    );
  }

  return (
    <div
      className={className}
      style={{
        WebkitBackgroundSize: "cover",
        MozBackgroundSize: "cover",
        OBackgroundSize: "cover",
      }}
    >
      <div className="h-full w-full bg-[var(--muted-foreground)] rounded-lg flex flex-col content-center items-center justify-items-center justify-center">
        {header && (
          <h3 className="text-popover text-base md:text-xs font-bold text-center">
            {header}
          </h3>
        )}
        {subHeader && (
          <h4 className="text-muted text-sm md:text-xs p-2">{subHeader}</h4>
        )}
        {text && (
          <p className="bg-white rounded m-2 text-foreground p-2 text-xs md:text-xs">
            {text}
          </p>
        )}
      </div>
    </div>
  );
}
