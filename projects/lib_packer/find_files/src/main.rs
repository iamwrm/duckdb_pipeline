use std::fs::File;
use std::io::{self, BufRead};
use regex::Regex;

#[derive(Debug)]
struct FileLine {
    file: String,
    line: String,
}

fn process_line(line: &str, re: &Regex) -> Option<FileLine> {
    for cap in re.captures_iter(line) {
        if let Some(file_path) = cap.get(2) {
            let path = file_path.as_str().to_string();
            return Some(FileLine {
                file: path,
                line: line.to_string(),
            });
        }
    }
    None
}


fn main() -> io::Result<()> {
    // Create regex pattern for matching system calls and their paths
    let re = Regex::new(r#"(?m)(open|openat|stat|access|execve)\(.*?"([^"]+)"#).unwrap();
    
    // Read the file line by line
    let file = File::open("../strace_output.txt")?;
    let reader = io::BufReader::new(file);

    let file_lines: Vec<_> = reader
        .lines()
        .filter_map(Result::ok)
        .filter_map(|line| process_line(&line, &re))
        .collect();

    // Print results
    println!("Found files:");
    for file_line in file_lines {
        dbg!(&file_line);
    }

    Ok(())
}