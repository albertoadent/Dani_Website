/* TEMPLATE secondary */

import InfoCardMain from "../Cards/InfoCard";
import { InfoCardSecondary } from "../Cards/InfoCard";

export default function SecondaryTemplate({ page }) {
  const contentSections = (page?.content || []).reduce(
    (outputArr, content, index) => {
      if (index % 3 == 0) {
        return [...outputArr, [content]];
      }
      outputArr[outputArr.length - 1].push(content);
      return outputArr;
    },
    []
  );

  console.log(contentSections);

  return (
    <div className="flex flex-col gap-y-4 p-6">
      {page?.content &&
        contentSections.map((array, index) => {
          return (
            <div>
              <InfoCardMain
                header={array[0].header}
                subHeader={array[0].subHeader}
                text={array[0].text}
                imageUrl={array[0].imageUrl}
                index={index}
                linkTo={array[0].linkTo}
              />
              <div className="flex justify-center my-2 bg-card p-2 rounded border-accent border-2">
                {array[1] && (
                  <InfoCardSecondary
                    header={array[1].header}
                    subHeader={array[1].subHeader}
                    text={array[1].text}
                    imageUrl={array[1].imageUrl}
                    index={index}
                    linkTo={array[1].linkTo}
                  />
                )}
                {array[2] && (
                  <InfoCardSecondary
                    header={array[2].header}
                    subHeader={array[2].subHeader}
                    text={array[2].text}
                    imageUrl={array[2].imageUrl}
                    index={index}
                    linkTo={array[2].linkTo}
                  />
                )}
              </div>
            </div>
          );
        })}
    </div>
  );
}
