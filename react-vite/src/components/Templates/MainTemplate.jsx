/* TEMPLATE 1 */

import MainCard from "../Cards/MainCard";

export default function MainTemplate({ page }) {
  return (
    <div className="grid grid-cols-2 gap-y-10 gap-x-2 p-10">
      {page?.content &&
        page.content.map(
          ({ header, subHeader, text, imageUrl, linkTo }, index) => (
            <div
              key={index}
              className="flex justify-center p-2 h-80 overflow-hidden rounded"
            >
              <MainCard
                header={header}
                subHeader={subHeader}
                text={text}
                imageUrl={imageUrl}
                index={index}
                linkTo={linkTo}
              />
            </div>
          )
        )}
    </div>
  );
}
