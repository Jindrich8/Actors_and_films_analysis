const cheerio = require("cheerio");
const fs = require("fs");
const path = require("path");


function saveCSV(filePath, content) {
    fs.mkdir(path.dirname(filePath), { recursive: true }, (err) => {
        if (err) {
            return console.error(err);
        }
        console.log('Directory created successfully!');
        fs.writeFile(filePath, content, "utf-8", (err) => {
            if (err) throw err;
            console.log('The file has been saved!');
        });
    });

}

/**
 * 
 * @param {string} separator 
 * @param {Number} limit 
 * @param {(relUrl : string) => Promise<CheerioAPI>} fetchFunc 
 * @returns {Promise<string>}
 */
async function getCSV(separator = ';', limit, fetchFunc) {
    let count = 0;
    const rows = [];
    const promises = [];
    const trSelector = "#page_filling_chart > center > table tr";

    let $ = await fetchFunc(count + 1);
    let trs = $(trSelector).toArray();
    // hlavička
    const header = $(trs.shift()).find("th").map((_, th) => $(th).text().trim()).get();
    header.push("BirthYear");
    rows.push(header);


    while (true) {
        for (let i = 0; i < trs.length && count < limit; ++i) {
            const tr = trs[i];
            const texts = $(tr).find("td,th").map((_, td) => $(td).text().trim()).get();
            const link = $(tr).find("a").first();
            if (texts.length < 1) {
                continue;
            }

            let href = null;

            if (link != null && (href = link.attr("href")) != null) {
                promises.push(fetchFunc(href));
            }
            else {
                promises.push(null);
            }


            ++count;
            rows.push(texts);
        }
        if (count >= limit) {
            break;
        }
        $ = await fetchFunc(count + 1);
        trs = $(trSelector).toArray().slice(1);
    }
    const apis = await Promise.all(promises);
    return rows.map((row, idx) => {
        if (idx > 0) {
            let $ = apis[idx - 1];
            if ($ != null) {
                const bornYear = getBornYear($);
                if (bornYear != null) {
                    row.push(bornYear);
                }
                else {
                    console.log(`${row[1]} birthYear is null`)
                }
            }
            else {
                console.log(`${row[1]} api is null`)
            }
        }
        return row.join(separator);
    }).join("\n");
}

/**
 * 
 * @param {CheerioAPI} $ 
 * @returns {string|null}
 */
function getBornYear($) {

    // vyhledání elementu
    const bornRow = $("#col2mid > table tr").filter((_, tr) => {
        return $(tr).text().includes("Born:");
    }).first();

    if (!bornRow) return null;

    // z něj vyber první <a>
    const el = bornRow.find("a").first();

    const text = el.text().trim();

    // aplikace regexu pro výběr roku
    const match = text.match(/(?<![0-9])([0-9]{4})(?![0-9])/);
    return match ? match[1] : null;
}


/**
 * 
 * @param {string} url 
 * @param {string|undefined} separator 
 * @param {number} limit 
 * @returns {Promise<string>}
 */
async function getMultiPageCSV(url, separator, limit) {
    return getCSV(separator, limit, async (nextRow) => {
        const currUrl = new URL(nextRow, url);
        console.log(currUrl.href);
        return cheerio.fromURL(currUrl);
    });
}

/**
 * 
 * @param {Date} date 
 * @returns {string}
 */
function getUTCDateSuffix(date) {
    const utcYear = date.getUTCFullYear();
    // Returns month between 0 and 11, so 1 must be added.
    const utcMonth = date.getUTCMonth() + 1;
    const utcDay = date.getUTCDate();
    return `${utcYear}-${utcMonth}-${utcDay}`;

}

const url = "https://www.the-numbers.com/box-office-star-records/domestic/lifetime-acting/top-grossing-leading-stars/";
const dateSuffix = getUTCDateSuffix(new Date());
getMultiPageCSV(url, ";", 200).then(csv =>
    saveCSV(`../data/original_data/popular_actors_${dateSuffix}.csv`, csv)
);
