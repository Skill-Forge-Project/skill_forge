import React from "react";
import CodeMirror from "@uiw/react-codemirror";
import { javascript } from "@codemirror/lang-javascript";
import { python } from "@codemirror/lang-python";
import { java } from "@codemirror/lang-java";
import { csharp } from "@replit/codemirror-lang-csharp";

const getLanguageExtension = (lang) => {
  switch (lang.toLowerCase()) {
    case "python":
      return python();
    case "javascript":
      return javascript({ jsx: true });
    case "java":
      return java();
    case "csharp":
    case "c#":
      return csharp();
    default:
      return javascript(); // default fallback
  }
};

const CodeEditor = ({ language = "javascript", code, onChange }) => {
  const handleChange = React.useCallback(
    (val) => {
      onChange(val);
    },
    [onChange]
  );

  return (
    <CodeMirror
      value={code}
      height="300px"
      theme="dark"
      extensions={[getLanguageExtension(language)]}
      onChange={handleChange}
    />
  );
};

export default CodeEditor;
