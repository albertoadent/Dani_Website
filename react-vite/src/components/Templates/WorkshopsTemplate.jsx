/* TEMPLATE workshops */

import WorkshopCard from "../Cards/WorkshopCard";

export default function WorkshopsTemplate({ page }) {
  return (
    <div className="mt-32 top-1">
      <h1 className="fixed top-[5.7rem] left-[50%] transform -translate-x-1/2 -translate-y-1/2 justify-center bg-card text-popover border-t-0 border-r-2 border-b-2 border-l-2 border-accent rounded-lg text-xl font-bold p-2 z-0">
        Workshops
      </h1>
      <div className="w-3/5 m-auto flex flex-col justify-center items-center align-center border-l-8 border-r-8 border-t-8 rounded-t-lg border-input">
        {page?.content &&
          page.content.map(
            ({ header, subHeader, text, imageUrl, linkTo }, index) => (
              <WorkshopCard
                header={header}
                subHeader={subHeader}
                text={text}
                linkTo={linkTo}
                index={index}
                imageUrl={imageUrl}
              />
            )
          )}
      </div>
    </div>
  );
}
